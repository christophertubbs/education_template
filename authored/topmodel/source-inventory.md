---
handoff_version: "1.0"
status: "in_review"
---
# Bounded repository inventory

Exact command: `git -C repository/topmodel ls-tree -r -l HEAD`.
Commit: `89e4dc529dfdf7f23b7365530973e9f238fb740d`.
This inventory reads Git metadata only. Inspection decisions and omissions are
recorded in `source-analysis.md`; presence here does not mean contents were read.
Review method: deterministic tree extraction. Result: 94 files and 3 gitlinks. No acceptance claim.

| Path | Git object | Bytes | Kind |
| --- | --- | --- | --- |
| .gitattributes | 3d432e03f1fc7b09a5dfa553223f0ae17d20b9d1 | 26 | blob |
| .github/ISSUE_TEMPLATE.md | 63a2ff5ada1c17ed3122b2289ba452c4d1d4a023 | 186 | blob |
| .github/PULL_REQUEST_TEMPLATE.md | 69d40bb976f1aa76fecf33e692a69d2ef7e5fca9 | 1351 | blob |
| .github/actions/build-boost/action.yml | 8bff17df0df784aac670b29397cb0844c08ea040 | 1790 | blob |
| .github/workflows/build_and_run_unit_test.yml | 799c066d125269579ff39ada9ddf7606c64d56d0 | 2417 | blob |
| .github/workflows/ngen_integration.yaml | 56dfd6d3207fffd8cc56b59d03228b37820cd4a0 | 4768 | blob |
| .gitignore | cd5ee98acf247ff24dc61bb764efcf25e44edf8a | 1574 | blob |
| .gitmodules | 8a59f1ee086e0a2d512b791dfbfd79c519811d3e | 340 | blob |
| CHANGELOG.md | e47878c8e9d568fca46bc64d58a719c4d65e7579 | 280 | blob |
| CMakeLists.txt | 1522e74cf4cfc8473cbce5f3ce767ff4fd93d103 | 5574 | blob |
| CONTRIBUTING.md | 0f109b26f9cd731fabdf72551a95b5cfe2ef863a | 1312 | blob |
| INSTALL.md | 9434f5eeb6971b4cf7e88b1ba4cf7c9f0d50d64a | 582 | blob |
| LICENSE | d645695673349e3947e8e5ae42332d0ac3164cd7 | 11358 | blob |
| README.md | ca09dafdde07ef89e5234da01ac75a7d55ea1da0 | 1747 | blob |
| SECURITY.md | 0cdd1d99dfaa8a93fc82c66be127e79e666b6bab | 3303 | blob |
| TERMS.md | b49b176bef3eced3d7ab0c9863223e872f57e739 | 1516 | blob |
| data/inputs.dat | b6ced36a84e525a585beb27b01edeedeee9dcc50 | 47202 | blob |
| data/params.dat | bd91898b330555a5ae551673245a8312bc6ab411 | 127 | blob |
| data/realization_config_topmodel_ngenCI.json | fe6106e9323aabdfaa6d64852e3ae18778df8976 | 4113 | blob |
| data/realization_config_topmodel_pet_ngen.json | 239e8fa187f69c26fa04227a1e87ca8fded306b4 | 2552 | blob |
| data/subcat.dat | 28ea4e418ac04697b552c85e4765917835731e4c | 771 | blob |
| data/topmod.run | 156547000d528ded0cd83416c16a8855a9ea9eea | 127 | blob |
| docs/BMI_ADAPTION.md | a4885db6c8a901fe634c934bd1cb69eca41551c3 | 10651 | blob |
| docs/INPUT_FILES_EXPLAINED.md | 2390847c20d5a3c3c73e064c3f07f9800481463b | 6212 | blob |
| docs/OUTPUT_FILES_EXPLAINED.md | 83070185e266990badefe6f858b37b73d52f7973 | 1963 | blob |
| docs/STAND_ALONE.md | 0bfc24971ea5bd61f660adbe486e7c04b0d6c109 | 4434 | blob |
| docs/VARIABLE_ROLES.md | 76795b0eb8f2a6d16e560bef2c7aa22983b07ac5 | 11197 | blob |
| docs/img/bmi_topmod_compare_hyd.png | 72febe7bf2d146b72d3c3680add4a0f4bd2837b4 | 37924 | blob |
| docs/img/bmi_topmod_compare_hyd_qobs.png | 02feb1bdd117a169c49c6bd12656495117b3bff2 | 55098 | blob |
| docs/img/bmi_topmod_compare_scatter.png | 65b7547a984e498804de56d8c52551f79448ae19 | 41728 | blob |
| docs/img/hyd_out.PNG | 8a0f3d532ea915085888267709a0177a15a1741e | 86852 | blob |
| docs/img/inputs_dat.PNG | 939103e4c9e46d5bd8b7bfe863d03549f2ace61e | 51783 | blob |
| docs/img/params_dat.PNG | 36c11a23b735a4fa1622aad363cab6c659b7e752 | 27139 | blob |
| docs/img/subcat_dat.PNG | 96321325bc9a6640eb179a075773cf3ed961fc56 | 80749 | blob |
| docs/img/topmod_out.PNG | 3cff5ee7cbc25bb60a96f43dbbb7f4580596041d | 242891 | blob |
| docs/img/topmod_run.PNG | a3e224d37173acedc80ff573983ae7ddf9034d9c | 38510 | blob |
| include/bmi.h | 6ea503089378f0c4eeb1d6c7879c610b5f69121f | 4891 | blob |
| include/bmi_serialization.h | c1b322bb8dfd7efd7b44f1a8ee77fb8a4528420f | 289 | blob |
| include/bmi_topmodel.h | 6bed3f5cdc4b890bbc36dfa78368e748ca93fd1a | 392 | blob |
| include/ngen_utilities.h | 3e31b592711b3da4b13a5b8bbac042b395d382d4 | 1876 | blob |
| include/topmodel.h | d957a27e46d3a0807c7cf11ec80a07c82d62ae0b | 10264 | blob |
| include/vecbuf.hpp | a20bc70e7326f8d4e94d68db6ae63cbf50e2ae9f | 5040 | blob |
| params/README.md | 98d27192a455bd7615f3ff454fe404bb34e32455 | 1874 | blob |
| params/data/hydrofabrics/releases/beta/01a/catchments.geojson | c6300fb16f597d7ffead72c328ceedcb3b647c19 | 71707010 | blob |
| params/data/hydrofabrics/releases/beta/01a/catchments_wgs84.json | 38b981e7334b288ae1d2f3dc9b63619574729341 | 75541352 | blob |
| params/data/hydrofabrics/releases/beta/01a/flowpaths.geojson | d356ff4b3c73229d9260e69be3b887e58bdbf99d | 69322276 | blob |
| params/data/hydrofabrics/releases/beta/01a/flowpaths_wgs84.json | 12e2ee8635c4ea856bb0b994ac4a044b5ce160a7 | 58599035 | blob |
| params/data/hydrofabrics/releases/beta/01a/gwbucket-params-fullrouting.csv | 1e7e3dfeb041954ef8b6e6225b5772a4158f7caa | 566641 | blob |
| params/data/hydrofabrics/releases/beta/01a/soil-properties-fullrouting.csv | 8281362e67433bd494fc76f0246a7400d2ba22e5 | 5895280 | blob |
| params/data/plots/AllWF.png | c2b242e41ea41819232333ebce1b40846a12664f | 122721 | blob |
| params/data/plots/AllWF_nclasses.txt | 4d68aae4d90aa5e18efecdb8667869b386bacfb3 | 320920 | blob |
| params/data/plots/Allgiuh.png | 342df3185334cee94b92211eb11da71954c75ea8 | 103182 | blob |
| params/data/plots/Allgiuh_nclasses.txt | b69cafbf0904702f252023f5bfa5eaa751c36c72 | 320946 | blob |
| params/data/plots/Alltwi.png | 45947f9aa5d773af86d352d3f49563862998b6cc | 52598 | blob |
| params/data/plots/Alltwi_nclasses.txt | 71b51e1d6c475cd7dbaa0a1ad4d851a98b47cd41 | 323144 | blob |
| params/others/RemoveFile.sh | db50967b7c0053dfbd00c6284b86574dcb4dde92 | 446 | blob |
| params/others/Run_topmodel.py | e622856cc60070dd2fff9f834584925a77e1c9b8 | 3982 | blob |
| params/others/summarize_results_V2.py | 8fc1d1a1dcb2c8adaba7897dbedc12654869dcaa | 1658 | blob |
| params/others/summarize_results_functions.py | 4fa6e9246344488a3b732b4dced212e1e5427b57 | 4708 | blob |
| params/src/generate_giuh_per_basin_params.py | 0ec02fb7f175c9a9c480b06545eac851532ff4e4 | 18367 | blob |
| params/src/generate_travel_time_by_pixel.py | e276889cdf656a15873ffac93555a61b3acf72df | 9307 | blob |
| params/src/generate_twi_per_basin.py | 55ad9070f6a7ae97b25b27f1de660c6c8d4e98c2 | 18527 | blob |
| params/src/workflow_hand_twi_giuh.env | 5baf0056f07624b0b76d828a39d0cbd98dc5ace2 | 2095 | blob |
| params/src/workflow_hand_twi_giuh.sh | 1ff73f5c865d60c0f443f201955c4c497c5b17d0 | 11414 | blob |
| refs/csdms/bmi-builder | fafe5b3704b3313f4b43ddc6cc8dff665705a079 | not applicable | commit |
| refs/csdms/bmi-c | d28c46d5b293935e51b8a88a23d0d843ecd32769 | not applicable | commit |
| refs/csdms/bmi-example-c | 93e9ef960d2e4d5132fba638e445379a20ac0259 | not applicable | commit |
| refs/original_code_c/README.1ST | 4a076ae7dfdc7da107b1392da07d2d9fc1925e1c | 1607 | blob |
| refs/original_code_c/demo_hydrograph.out | b875f8b386bb6792ff22e4c47a72193c18e8019a | 20792 | blob |
| refs/original_code_c/demo_topmod.out | 989e934d333ab2044cad9d7d49c535ca5cb96a3f | 77750 | blob |
| refs/original_code_c/inputs.dat | b6ced36a84e525a585beb27b01edeedeee9dcc50 | 47202 | blob |
| refs/original_code_c/params.dat | bd91898b330555a5ae551673245a8312bc6ab411 | 127 | blob |
| refs/original_code_c/subcat.dat | 28ea4e418ac04697b552c85e4765917835731e4c | 771 | blob |
| refs/original_code_c/tmod9502.c | 86302416c1482568478e7655c3699724be5c5e9d | 36553 | blob |
| refs/original_code_c/topmod.run | 705deeb8d84ffa4d5911775cc2648c7775dfdf60 | 111 | blob |
| refs/original_code_fortran/TMOD9502.f | 6737b2638db7ccebd4e004ba6128fe21ae6c7395 | 22455 | blob |
| refs/original_code_fortran/a.out | 9f708683f2fe573f5e8446b2b1233b671ee83533 | 41277 | blob |
| refs/original_code_fortran/atb.dat | 4b03cba662f7be7a522319c930f7a12f34984f71 | 247 | blob |
| refs/original_code_fortran/demo_topmod.out | a9a18201393e678257ad31c70eb67f97f7494d0c | 73229 | blob |
| refs/original_code_fortran/input.dat | 3316c02a754bd1e7e967fe8e682b68a519d0e2e3 | 1394 | blob |
| refs/original_code_fortran/inputs.dat | c7e224739827f005f7b946c93bab02cb58645137 | 45770 | blob |
| refs/original_code_fortran/params.dat | 50b328142bae708e775140c9d0a46a242737e7ee | 124 | blob |
| refs/original_code_fortran/subcat.dat | d0680e26038543c60c133f27a450f2c9d83043b8 | 731 | blob |
| refs/original_code_fortran/topmod.run | 20c5370abc932c4b3ddbefd4a3b0d37632ba21f1 | 97 | blob |
| src/bmi_serialization.cpp | bd207ba21298b6f5ab608e742cdbc0a3143e2b1f | 7676 | blob |
| src/bmi_topmodel.c | 03d2a6f80e4387522d4615e25ae7116a3ac99b7c | 46700 | blob |
| src/main.c | 3905c427b269149e2cc20560b6b71af1f8a2afda | 2053 | blob |
| src/topmodel.c | c8a79cba3d889ae07e97c83765e1b10d78c5a73e | 47179 | blob |
| test/README.md | 01d54b9bfb5cbf92c8af79d2fb1e5abcc4f94ca1 | 3441 | blob |
| test/data/inputs.dat | b6ced36a84e525a585beb27b01edeedeee9dcc50 | 47202 | blob |
| test/data/params.dat | bd91898b330555a5ae551673245a8312bc6ab411 | 127 | blob |
| test/data/subcat.dat | 89be1c56abaffb01a85b93049f572170193addf3 | 771 | blob |
| test/data/topmod.run | 995faa72d7ce73b45bea06a98b30b11b0f80159e | 125 | blob |
| test/data/topmod_unit_test.run | d6c669541b3e8763a77d41e7506c171b8c284205 | 143 | blob |
| test/main_integration_test_serialization.c | da6cb0bf5d61368f1a993d97a7db1c8737f4648b | 8335 | blob |
| test/main_unit_test_bmi.c | eb6fcd39772268b21d7431483878a6a8d9a872a6 | 16773 | blob |
| test/main_unit_test_serialization.c | d9f9f1a4188edbf75106be15ccb7a07440e08368 | 21766 | blob |

