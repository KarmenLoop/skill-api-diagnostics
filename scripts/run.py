"""Classify API failures and choose bounded, replay-aware next steps."""
from runtime import *

from urllib.parse import urlsplit
def process(data):
    endpoint=urlsplit(text(data["endpoint"],"endpoint"))
    if endpoint.scheme not in ("http","https") or not endpoint.hostname: raise ValueError("endpoint must be HTTP(S)")
    host=endpoint.hostname
    if ":" in host: host="["+host+"]"
    port=(":"+str(endpoint.port)) if endpoint.port else ""
    sanitized=endpoint.scheme+"://"+host+port+endpoint.path
    budget=number(data["budget_seconds"],"budget_seconds",0)
    elapsed=number(data["elapsed_seconds"],"elapsed_seconds",0)
    if type(data["replay_safe"]) is not bool: raise ValueError("replay_safe must be boolean")
    attempts=records(data,"attempts")
    unique(attempts)
    if not attempts: raise ValueError("provide at least one attempt")
    for row in attempts:
        status=row.get("status")
        if status is not None:
            integer(status,"status",100)
            if status>599: raise ValueError("status exceeds 599")
        choice(row.get("error_kind","none"),("dns","tls","timeout","connection","context","quota","none"),"error_kind")
        number(row.get("retry_after_seconds",1),"retry_after_seconds",0)
    last=attempts[-1]
    status=last.get("status")
    error=last.get("error_kind","none")
    category="unknown"
    action="Inspect the original sanitized response and transport stage."
    transient=False
    if error=="context" or status==413: category,action="context","Check actual model capacity; reduce or chunk the request."
    elif status in (401,403): category,action="authentication","Check credential source, project access, and endpoint permissions."
    elif error=="quota": category,action="quota","Check the provider's available credits and hard quota; do not retry unchanged."
    elif status==429: category,action,transient="rate_limit","Honor Retry-After after confirming this is a transient rate limit.",True
    elif status is not None and 500<=status<=599: category,action,transient="server","Retry only within budget and the operation's replay contract.",True
    elif error in ("timeout","connection"): category,action,transient=error,"Check transport and whether the request was already dispatched.",True
    elif error=="dns": category,action="dns","Verify hostname, resolver, and network configuration."
    elif error=="tls": category,action="tls","Fix certificate or proxy trust; keep TLS verification enabled."
    elif status is not None and 200<=status<300: category,action="success","Validate response content and any tool results."
    elif status is not None and 400<=status<500: category,action="request","Check protocol, route, model ID, and request schema."
    delay=last.get("retry_after_seconds",1)
    remaining=max(0,budget-elapsed)
    retry=transient and data["replay_safe"] and delay<remaining
    if transient and not data["replay_safe"]: action="Verify the original outcome before repeating this operation."
    elif transient and not retry: action="Stop: the total retry budget is exhausted."
    return {"category":category,"next_action":action,"retry_allowed":retry,"retry_delay_seconds":delay if retry else None,"endpoint":sanitized,"attempt_count":len(attempts),"remaining_budget_seconds":remaining}

if __name__ == "__main__":
    sys.exit(main(process, "Classify API failures and choose bounded, replay-aware next steps."))
