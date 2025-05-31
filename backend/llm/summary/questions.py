def get_question():
    return [
        {
            "section": "Supplier Details",
            "data": [
                {
                    "q": """what is the supplier name. Format the result only the exact name of the supplier""",
                    "title": "Supplier Name",
                },
                {
                    "q": """what is the supplier address. Format the result only the exact address of the supplier""",
                    "title": "Supplier Address",
                },
                {
                    "q": """what is the Supplier Type. Format the result only the exact Type of the supplier""",
                    "title": "Supplier Type",
                },
                {
                    "q": """what is the Contact Person of the supplier. Format the result only the exact Contact Person of the supplier""",
                    "title": "Contact Person",
                },
                {
                    "q": """what is the Contact Email of the supplier. Format the result only the exact Contact Email of the supplier""",
                    "title": "Contact Email",
                },
                {
                    "q": """what is the Quality Rating of the INTERNAL ASSESSMENT. Format the result only the exact Quality Rating of the INTERNAL ASSESSMENT with prepend \"Score \"""",
                    "title": "Quality Rating",
                },
                {
                    "q": """what is the Supply Risk Level of the INTERNAL ASSESSMENT. Format the result only the exact Supply Risk Level of the INTERNAL ASSESSMENT""",
                    "title": "Supply Risk Level",
                },
            ]
        },
        # {
        #     "section": "Reporter Summary",
        #     "data": [
        #         {
        #             "q": "Author details of this literature?", #"Please provide the summary of basic Reporter or Author information like name, address, occupation and country?",
        #             "summary": True,
        #         }
        #     ]
        # },
        # {
        #     "section": "Patient Summary",
        #     "data": [
        #         {
        #             "q": "Please provide the details of the patients who have been treated with this drug",
        #             "summary": True,
        #         },
        #         # {
        #         #     "q": "If possible, show the result with other info if avaliable like name, country of residence, Age, Date of Birth, weight, height, gender and detailed address who has experienced the adverse event?",
        #         #     "summary": True,
        #         # },
        #         # {
        #         #     "q": "Please provide the summary of any other relevant history available for the patient or direct family or Parent information? If yes, then specify the Start Date, End Date, Adverse Event details for them?",
        #         #     "summary": True,
        #         # },
        #     ]
        # },
        # {
        #     "section": "Adverse Reaction Summary",
        #     "data": [
        #         {
        #             "q": "Provide me the summary of event or indication or reaction or side effect",
        #             "summary or is there any serious adverse event shown by the patients as a result of the treatment": True,
        #         },
        #         # {
        #         #     "q": "Provide me the summary of event or indication or reaction or side effect",
        #         #     "summary or is there any serious adverse event shown by the patients as a result of the treatment": True,
        #         # },
        #     ]
        # }
    ]
