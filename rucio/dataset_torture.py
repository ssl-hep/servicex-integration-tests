# Dataset "torture" test for the Rucio DID finder.
#
# Purpose:
#   Stress the ServiceX dataset cache / DID lookup path by submitting several
#   transform requests at once that all target the SAME Rucio dataset
#   (DAOD_PHYSLITE, limited to 2 files) but with slightly different queries.
#   This checks that concurrent requests for one DID are handled correctly
#   (a single lookup/registration, no duplicate-dataset races or failures).
#
# Steps:
#   1. Look up any previously cached dataset for this DID
#      ("rucio://<did>?files=2") on the server and delete it, so the test
#      always starts from a cold cache.
#   2. Build a spec with five samples (zmumu .. zmumu5). Each uses an UprootRaw
#      query on the CollectionTree, selecting the AnalysisMuonsAuxDyn muon
#      branches (pt, eta, phi, charge, quality, isolation variables) and applying
#      a slightly different event cut on muon pT (and multiplicity for the first
#      two), so every request is a distinct transform on the same dataset.
#   3. Submit all samples with deliver(), bypassing the local cache, and
#      request the output as root-rntuple.
#   4. Assert that results for "zmumu" and "zmumu2" are present and that each
#      returned exactly 2 output files.
#
# Requires a configured ServiceX endpoint with Rucio access (servicex.yaml).

import sys

import typer

from servicex import query, dataset, deliver
from servicex.servicex_client import ServiceXClient

ds_name = "data25_13p6TeV:data25_13p6TeV.00500014.physics_Main.deriv.DAOD_PHYSLITE.f1591_m2272_p6828"
sx = ServiceXClient()

filtered = list(filter(lambda ds: ds.name == 'rucio://'+ds_name+"?files=2", list(sx.get_datasets(did_finder="rucio"))))
print(f"found {len(filtered)} datasets")
assert len(filtered) <= 1
if len(filtered) == 1:
    dataset_id = filtered[0].id
    print("Removing existing dataset")
    result = sx.delete_dataset(dataset_id)
    if result:
        typer.echo(f"Dataset {dataset_id} deleted")
    else:
        typer.echo(f"Dataset {dataset_id} not found")

spec = {'General': {'OutputFormat': 'root-rntuple',
                    },
        'Sample': [{'Name': 'zmumu',
                    'Dataset': dataset.Rucio(ds_name),
                    'Query': query.UprootRaw({'treename': 'CollectionTree',
                                              'filter_name': [
                                                  '/AnalysisMuonsAuxDyn.(pt|eta|phi|charge|quality)/i',
                                                  '/AnalysisMuonsAuxDyn.(ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt500|neflowisol20)/i'],
                                              'cut': 'count_nonzero(AnalysisMuonsAuxDyn.pt >= 10e3) >= 2'
                                              }
                                             ),
                    'NFiles': 2,
                    },
                   {'Name': 'zmumu2',
                    'Dataset': dataset.Rucio(ds_name),
                    'Query': query.UprootRaw({'treename': 'CollectionTree',
                                              'filter_name': [
                                                  '/AnalysisMuonsAuxDyn.(pt|eta|phi|charge|quality)/i',
                                                  '/AnalysisMuonsAuxDyn.(ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt500|neflowisol20)/i'],
                                              'cut': 'count_nonzero(AnalysisMuonsAuxDyn.pt >= 10e3) >= 1'
                                              }
                                             ),
                    'NFiles': 2,
                    },
                   {'Name': 'zmumu3',
                    'Dataset': dataset.Rucio(ds_name),
                    'Query': query.UprootRaw({'treename': 'CollectionTree',
                                              'filter_name': [
                                                  '/AnalysisMuonsAuxDyn.(pt|eta|phi|charge|quality)/i',
                                                  '/AnalysisMuonsAuxDyn.(ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt500|neflowisol20)/i'],
                                              'cut': 'count_nonzero(AnalysisMuonsAuxDyn.pt >= 10.1e3) >= 1'
                                              }
                                             ),
                    'NFiles': 2,
                    },
                   {'Name': 'zmumu4',
                    'Dataset': dataset.Rucio(ds_name),
                    'Query': query.UprootRaw({'treename': 'CollectionTree',
                                              'filter_name': [
                                                  '/AnalysisMuonsAuxDyn.(pt|eta|phi|charge|quality)/i',
                                                  '/AnalysisMuonsAuxDyn.(ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt500|neflowisol20)/i'],
                                              'cut': 'count_nonzero(AnalysisMuonsAuxDyn.pt >= 10.2e3) >= 1'
                                              }
                                             ),
                    'NFiles': 2,
                    },
                   {'Name': 'zmumu5',
                    'Dataset': dataset.Rucio(ds_name),
                    'Query': query.UprootRaw({'treename': 'CollectionTree',
                                              'filter_name': [
                                                  '/AnalysisMuonsAuxDyn.(pt|eta|phi|charge|quality)/i',
                                                  '/AnalysisMuonsAuxDyn.(ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt500|neflowisol20)/i'],
                                              'cut': 'count_nonzero(AnalysisMuonsAuxDyn.pt >= 10.3e3) >= 1'
                                              }
                                             ),
                    'NFiles': 2,
                    }
                   ]
        }

results = deliver(spec, ignore_local_cache=True)
print(results)
assert "zmumu" in results
assert "zmumu2" in results

assert len(results["zmumu"]) == 2
assert len(results["zmumu2"]) == 2