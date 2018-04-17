# API Documentation

## Endpoint

- [GET /api/asset](#Asset)
- [GET /api/plan](#Plan)
- [GET /api/report](#Report)

## Data Structure

### Asset

```
{
    asset.id -> (int): {
        "name": asset.name -> (str),
        "availability": asset.availability -> (int),
    },
    ...
}
```
### Plan

```
[
    {
        "id": plan.id -> (int),
        "crisis_id": plan.crisis_id -> (int),
        "details": plan.details -> (str) -> "((asset.id, number),...)",
        "time": plan.time -> (str) -> "YYYY-MM-DD HH:mm:ss",
        "progress": plan.progress -> (int) -> (-1=not-yet-executed, 0=in-progress, 1=finished)
    },
    ...
]
```
### Report

```
[
    {
        "report_id": report.id -> (int),
        "crisis_id": report.crisis_id -> (int),
        "assets_used": report.assets_used_parsed -> (str) -> "((asset.id, number),...)",
        "casualty": report.casualty_parsed -> (str) -> "((asset.id, number),...)",
        "details": report.details -> (str),
        "is_final": report.is_final -> ("True" or "False"),
        "time": report.time -> (str) -> "YYYY-MM-DD HH:mm:ss",
    },
    ...
]
```
> **NOTES**
>
> casualty will be an empty string when there's no casualty
>
> Asset_used and casualty is a cumulative value for one crisis
