import boto3
import pandas as pd
from datetime import datetime

client = boto3.client("inspector2")

all_findings = []

paginator = client.get_paginator("list_findings")

for page in paginator.paginate(
filterCriteria={
"findingStatus": [{"comparison": "EQUALS", "value": "ACTIVE"}]
}
):
for finding in page["findings"]:

```
    resource_id = "N/A"
    if finding.get("resources"):
        resource_id = finding["resources"][0].get("id", "N/A")

    cve = "N/A"
    if finding.get("packageVulnerabilityDetails"):
        cve = finding["packageVulnerabilityDetails"].get("vulnerabilityId", "N/A")

    all_findings.append({
        "Title": finding.get("title"),
        "Severity": finding.get("severity"),
        "CVE": cve,
        "Resource ID": resource_id,
        "Resource Type": finding.get("type"),
        "First Observed": finding.get("firstObservedAt"),
        "Description": finding.get("description")
    })
```

df = pd.DataFrame(all_findings)

today = datetime.now().strftime("%Y-%m-%d")
file_name = f"inspector_report_{today}.xlsx"

df.to_excel(file_name, index=False)

print("Report generated:", file_name)
