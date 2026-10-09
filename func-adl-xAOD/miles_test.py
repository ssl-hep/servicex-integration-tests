from servicex import query as q, deliver, dataset


def func_adl_xaod_simple():
    query = q.FuncADL_ATLASr22()  # type: ignore
    jets_per_event = query.Select(lambda e: e.Jets("AnalysisJets"))
    jet_info_per_event = jets_per_event.Select(
        lambda jets: {
            "pt": jets.Select(lambda j: j.pt()),
            "eta": jets.Select(lambda j: j.eta()),
        }
    )

    spec = {
        "Sample": [
            {
                "Name": "func_adl_xAOD_simple",
                "Dataset": dataset.Rucio(
                        "mc23_13p6TeV:mc23_13p6TeV.801002.Py8EG_A14NNPDF23LO_Gammatautau_MassWeight.merge.AOD.e8514_e8528_e8586_s4481_s4370_r16685_r16695"
                ),
                "Query": jet_info_per_event,
            }
        ]
    }
    files = deliver(spec, servicex_name="servicex-uc-af")
    assert files is not None, "No files returned from deliver! Internal error"
    return files


if __name__ == "__main__":
    files = func_adl_xaod_simple()
    assert len(files["func_adl_xAOD_simple"]) == 1
