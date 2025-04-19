from pytrials.client import ClinicalTrials

ct = ClinicalTrials()

studies = ct.get_study_fields(
    search_expr="Tylenol",
    fields=["NCTId", "BriefTitle", "InterventionName","NumSecondaryId"],
    max_studies=10,
    fmt="json"
)

# Print the data
print("Clinical Trials Data:")

for study in studies["studies"]:
    protocol = study["protocolSection"]
    ident = protocol["identificationModule"]
    interventions = protocol["armsInterventionsModule"]["interventions"]

    print(f"NCT ID: {ident['nctId']}")

    print(ident)
    #numSecondaryIds
    print(f"Secondary IDs: {ident['secondaryId']}")
    print(f"Title: {ident['briefTitle']}")
    print("Interventions:")
    for i in interventions:
        print(f"  - {i['name']}")
    print("---")
