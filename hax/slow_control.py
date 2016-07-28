# Slow control interface
import datetime
import os

import pandas as pd

import pymongo

VARIABLES = {
    'cryogenics': {
        "cryostat_pressure_bar"                        : "XE1T.CRY_PT101_PCHAMBER_AI.PI",
        "LXe_temperature_bottom_C"                     : "XE1T.CRY_TE101_TCRYOBOTT_AI.PI",
        "LXe_temperature_above_bottom_PMTs_C"          : "XE1T.CRY_TE102_TCRYOBOTPMT_AI.PI",
        "vacuum_insolation_pressure_mbar"              : "XE1T.CRY_PI110_PT113_PINS_AI.PI",
        "GXe_circulation_mass_flow_to_getter_201_SLPM" : "XE1T.PUR_FC201_FMON.PI",
        "GXe_circulation_mass_flow_to_getter_202_SLPM" : "XE1T.PUR_FC201_FMON.PI",
        "GXe_mass_flow_to_the_bell_SLPM"               : "XE1T.CRY_FCV104FMON.PI",
        "Xe_height_above_gate_in_short_levelmeter_2_mm": "XE1T.GEN_CE912_SLM2_HMON.PI",
        "valve_state_V106"                             : "XE1T.CRY_V106_R_REQ2SCADA.ST"
    },
    'water' : { 'water_level_m' : "XE1T.WLP_INDLEVL_H20_1.PI" },
    'field'     : {
        'cathode_kV': 'XE1T.GEN_HEINZVMON.PI',
        'anode_V'   : 'XE1T.CTPC.BOARD14.CHAN000.VMON'
    },

    'pmts'      : {
        'pmt_000_bias_V': 'XE1T.CTPC.BOARD06.CHAN005.VMON',
        'pmt_001_bias_V': 'XE1T.CTPC.BOARD08.CHAN000.VMON',
        'pmt_002_bias_V': 'XE1T.CTPC.BOARD08.CHAN001.VMON',
        'pmt_003_bias_V': 'XE1T.CTPC.BOARD08.CHAN002.VMON',
        'pmt_004_bias_V': 'XE1T.CTPC.BOARD08.CHAN003.VMON',
        'pmt_005_bias_V': 'XE1T.CTPC.BOARD08.CHAN004.VMON',
        'pmt_006_bias_V': 'XE1T.CTPC.BOARD08.CHAN005.VMON',
        'pmt_007_bias_V': 'XE1T.CTPC.BOARD03.CHAN000.VMON',
        'pmt_008_bias_V': 'XE1T.CTPC.BOARD03.CHAN001.VMON',
        'pmt_009_bias_V': 'XE1T.CTPC.BOARD03.CHAN002.VMON',
        'pmt_010_bias_V': 'XE1T.CTPC.BOARD03.CHAN003.VMON',
        'pmt_011_bias_V': 'XE1T.CTPC.BOARD03.CHAN004.VMON',
        'pmt_012_bias_V': 'XE1T.CTPC.BOARD03.CHAN005.VMON',
        'pmt_013_bias_V': 'XE1T.CTPC.BOARD05.CHAN000.VMON',
        'pmt_014_bias_V': 'XE1T.CTPC.BOARD05.CHAN001.VMON',
        'pmt_015_bias_V': 'XE1T.CTPC.BOARD05.CHAN002.VMON',
        'pmt_016_bias_V': 'XE1T.CTPC.BOARD05.CHAN003.VMON',
        'pmt_017_bias_V': 'XE1T.CTPC.BOARD05.CHAN004.VMON',
        'pmt_018_bias_V': 'XE1T.CTPC.BOARD05.CHAN005.VMON',
        'pmt_019_bias_V': 'XE1T.CTPC.BOARD07.CHAN000.VMON',
        'pmt_020_bias_V': 'XE1T.CTPC.BOARD07.CHAN001.VMON',
        'pmt_021_bias_V': 'XE1T.CTPC.BOARD07.CHAN002.VMON',
        'pmt_022_bias_V': 'XE1T.CTPC.BOARD07.CHAN003.VMON',
        'pmt_023_bias_V': 'XE1T.CTPC.BOARD07.CHAN004.VMON',
        'pmt_024_bias_V': 'XE1T.CTPC.BOARD07.CHAN005.VMON',
        'pmt_025_bias_V': 'XE1T.CTPC.BOARD04.CHAN000.VMON',
        'pmt_026_bias_V': 'XE1T.CTPC.BOARD04.CHAN001.VMON',
        'pmt_027_bias_V': 'XE1T.CTPC.BOARD04.CHAN002.VMON',
        'pmt_028_bias_V': 'XE1T.CTPC.BOARD04.CHAN003.VMON',
        'pmt_029_bias_V': 'XE1T.CTPC.BOARD04.CHAN004.VMON',
        'pmt_030_bias_V': 'XE1T.CTPC.BOARD04.CHAN005.VMON',
        'pmt_031_bias_V': 'XE1T.CTPC.BOARD06.CHAN000.VMON',
        'pmt_032_bias_V': 'XE1T.CTPC.BOARD06.CHAN001.VMON',
        'pmt_033_bias_V': 'XE1T.CTPC.BOARD06.CHAN002.VMON',
        'pmt_034_bias_V': 'XE1T.CTPC.BOARD06.CHAN003.VMON',
        'pmt_035_bias_V': 'XE1T.CTPC.BOARD06.CHAN004.VMON',
        'pmt_036_bias_V': 'XE1T.CTPC.BOARD06.CHAN010.VMON',
        'pmt_037_bias_V': 'XE1T.CTPC.BOARD06.CHAN011.VMON',
        'pmt_038_bias_V': 'XE1T.CTPC.BOARD08.CHAN006.VMON',
        'pmt_039_bias_V': 'XE1T.CTPC.BOARD08.CHAN007.VMON',
        'pmt_040_bias_V': 'XE1T.CTPC.BOARD08.CHAN008.VMON',
        'pmt_041_bias_V': 'XE1T.CTPC.BOARD08.CHAN009.VMON',
        'pmt_042_bias_V': 'XE1T.CTPC.BOARD03.CHAN006.VMON',
        'pmt_043_bias_V': 'XE1T.CTPC.BOARD03.CHAN007.VMON',
        'pmt_044_bias_V': 'XE1T.CTPC.BOARD03.CHAN008.VMON',
        'pmt_045_bias_V': 'XE1T.CTPC.BOARD03.CHAN009.VMON',
        'pmt_046_bias_V': 'XE1T.CTPC.BOARD03.CHAN010.VMON',
        'pmt_047_bias_V': 'XE1T.CTPC.BOARD05.CHAN006.VMON',
        'pmt_048_bias_V': 'XE1T.CTPC.BOARD05.CHAN007.VMON',
        'pmt_049_bias_V': 'XE1T.CTPC.BOARD05.CHAN008.VMON',
        'pmt_050_bias_V': 'XE1T.CTPC.BOARD05.CHAN009.VMON',
        'pmt_051_bias_V': 'XE1T.CTPC.BOARD05.CHAN010.VMON',
        'pmt_052_bias_V': 'XE1T.CTPC.BOARD05.CHAN011.VMON',
        'pmt_053_bias_V': 'XE1T.CTPC.BOARD07.CHAN006.VMON',
        'pmt_054_bias_V': 'XE1T.CTPC.BOARD07.CHAN007.VMON',
        'pmt_055_bias_V': 'XE1T.CTPC.BOARD07.CHAN008.VMON',
        'pmt_056_bias_V': 'XE1T.CTPC.BOARD07.CHAN009.VMON',
        'pmt_057_bias_V': 'XE1T.CTPC.BOARD04.CHAN006.VMON',
        'pmt_058_bias_V': 'XE1T.CTPC.BOARD04.CHAN007.VMON',
        'pmt_059_bias_V': 'XE1T.CTPC.BOARD04.CHAN008.VMON',
        'pmt_060_bias_V': 'XE1T.CTPC.BOARD04.CHAN009.VMON',
        'pmt_061_bias_V': 'XE1T.CTPC.BOARD04.CHAN010.VMON',
        'pmt_062_bias_V': 'XE1T.CTPC.BOARD06.CHAN006.VMON',
        'pmt_063_bias_V': 'XE1T.CTPC.BOARD06.CHAN007.VMON',
        'pmt_064_bias_V': 'XE1T.CTPC.BOARD06.CHAN008.VMON',
        'pmt_065_bias_V': 'XE1T.CTPC.BOARD06.CHAN009.VMON',
        'pmt_066_bias_V': 'XE1T.CTPC.BOARD06.CHAN015.VMON',
        'pmt_067_bias_V': 'XE1T.CTPC.BOARD06.CHAN016.VMON',
        'pmt_068_bias_V': 'XE1T.CTPC.BOARD08.CHAN010.VMON',
        'pmt_069_bias_V': 'XE1T.CTPC.BOARD08.CHAN011.VMON',
        'pmt_070_bias_V': 'XE1T.CTPC.BOARD03.CHAN011.VMON',
        'pmt_071_bias_V': 'XE1T.CTPC.BOARD03.CHAN012.VMON',
        'pmt_072_bias_V': 'XE1T.CTPC.BOARD03.CHAN013.VMON',
        'pmt_073_bias_V': 'XE1T.CTPC.BOARD03.CHAN014.VMON',
        'pmt_074_bias_V': 'XE1T.CTPC.BOARD03.CHAN015.VMON',
        'pmt_075_bias_V': 'XE1T.CTPC.BOARD05.CHAN012.VMON',
        'pmt_076_bias_V': 'XE1T.CTPC.BOARD05.CHAN013.VMON',
        'pmt_077_bias_V': 'XE1T.CTPC.BOARD05.CHAN014.VMON',
        'pmt_078_bias_V': 'XE1T.CTPC.BOARD05.CHAN015.VMON',
        'pmt_079_bias_V': 'XE1T.CTPC.BOARD05.CHAN016.VMON',
        'pmt_080_bias_V': 'XE1T.CTPC.BOARD07.CHAN010.VMON',
        'pmt_081_bias_V': 'XE1T.CTPC.BOARD07.CHAN011.VMON',
        'pmt_082_bias_V': 'XE1T.CTPC.BOARD04.CHAN011.VMON',
        'pmt_083_bias_V': 'XE1T.CTPC.BOARD04.CHAN012.VMON',
        'pmt_084_bias_V': 'XE1T.CTPC.BOARD04.CHAN013.VMON',
        'pmt_085_bias_V': 'XE1T.CTPC.BOARD04.CHAN014.VMON',
        'pmt_086_bias_V': 'XE1T.CTPC.BOARD04.CHAN015.VMON',
        'pmt_087_bias_V': 'XE1T.CTPC.BOARD06.CHAN012.VMON',
        'pmt_088_bias_V': 'XE1T.CTPC.BOARD06.CHAN013.VMON',
        'pmt_089_bias_V': 'XE1T.CTPC.BOARD06.CHAN014.VMON',
        'pmt_090_bias_V': 'XE1T.CTPC.BOARD06.CHAN019.VMON',
        'pmt_091_bias_V': 'XE1T.CTPC.BOARD06.CHAN020.VMON',
        'pmt_092_bias_V': 'XE1T.CTPC.BOARD08.CHAN012.VMON',
        'pmt_093_bias_V': 'XE1T.CTPC.BOARD03.CHAN016.VMON',
        'pmt_094_bias_V': 'XE1T.CTPC.BOARD03.CHAN017.VMON',
        'pmt_095_bias_V': 'XE1T.CTPC.BOARD03.CHAN018.VMON',
        'pmt_096_bias_V': 'XE1T.CTPC.BOARD03.CHAN019.VMON',
        'pmt_097_bias_V': 'XE1T.CTPC.BOARD05.CHAN017.VMON',
        'pmt_098_bias_V': 'XE1T.CTPC.BOARD05.CHAN018.VMON',
        'pmt_099_bias_V': 'XE1T.CTPC.BOARD05.CHAN019.VMON',
        'pmt_100_bias_V': 'XE1T.CTPC.BOARD05.CHAN020.VMON',
        'pmt_101_bias_V': 'XE1T.CTPC.BOARD07.CHAN012.VMON',
        'pmt_102_bias_V': 'XE1T.CTPC.BOARD04.CHAN016.VMON',
        'pmt_103_bias_V': 'XE1T.CTPC.BOARD04.CHAN017.VMON',
        'pmt_104_bias_V': 'XE1T.CTPC.BOARD04.CHAN018.VMON',
        'pmt_105_bias_V': 'XE1T.CTPC.BOARD04.CHAN019.VMON',
        'pmt_106_bias_V': 'XE1T.CTPC.BOARD06.CHAN017.VMON',
        'pmt_107_bias_V': 'XE1T.CTPC.BOARD06.CHAN018.VMON',
        'pmt_108_bias_V': 'XE1T.CTPC.BOARD06.CHAN022.VMON',
        'pmt_109_bias_V': 'XE1T.CTPC.BOARD08.CHAN013.VMON',
        'pmt_110_bias_V': 'XE1T.CTPC.BOARD03.CHAN020.VMON',
        'pmt_111_bias_V': 'XE1T.CTPC.BOARD03.CHAN021.VMON',
        'pmt_112_bias_V': 'XE1T.CTPC.BOARD03.CHAN022.VMON',
        'pmt_113_bias_V': 'XE1T.CTPC.BOARD05.CHAN021.VMON',
        'pmt_114_bias_V': 'XE1T.CTPC.BOARD05.CHAN022.VMON',
        'pmt_115_bias_V': 'XE1T.CTPC.BOARD07.CHAN013.VMON',
        'pmt_116_bias_V': 'XE1T.CTPC.BOARD04.CHAN020.VMON',
        'pmt_117_bias_V': 'XE1T.CTPC.BOARD04.CHAN021.VMON',
        'pmt_118_bias_V': 'XE1T.CTPC.BOARD04.CHAN022.VMON',
        'pmt_119_bias_V': 'XE1T.CTPC.BOARD06.CHAN021.VMON',
        'pmt_120_bias_V': 'XE1T.CTPC.BOARD06.CHAN023.VMON',
        'pmt_121_bias_V': 'XE1T.CTPC.BOARD08.CHAN014.VMON',
        'pmt_122_bias_V': 'XE1T.CTPC.BOARD03.CHAN023.VMON',
        'pmt_123_bias_V': 'XE1T.CTPC.BOARD05.CHAN023.VMON',
        'pmt_124_bias_V': 'XE1T.CTPC.BOARD07.CHAN014.VMON',
        'pmt_125_bias_V': 'XE1T.CTPC.BOARD04.CHAN023.VMON',
        'pmt_126_bias_V': 'XE1T.CTPC.BOARD07.CHAN015.VMON',
        'pmt_127_bias_V': 'XE1T.CTPC.BOARD09.CHAN000.VMON',
        'pmt_128_bias_V': 'XE1T.CTPC.BOARD09.CHAN001.VMON',
        'pmt_129_bias_V': 'XE1T.CTPC.BOARD09.CHAN002.VMON',
        'pmt_130_bias_V': 'XE1T.CTPC.BOARD09.CHAN003.VMON',
        'pmt_131_bias_V': 'XE1T.CTPC.BOARD09.CHAN004.VMON',
        'pmt_132_bias_V': 'XE1T.CTPC.BOARD11.CHAN000.VMON',
        'pmt_133_bias_V': 'XE1T.CTPC.BOARD11.CHAN001.VMON',
        'pmt_134_bias_V': 'XE1T.CTPC.BOARD09.CHAN005.VMON',
        'pmt_135_bias_V': 'XE1T.CTPC.BOARD09.CHAN006.VMON',
        'pmt_136_bias_V': 'XE1T.CTPC.BOARD09.CHAN007.VMON',
        'pmt_137_bias_V': 'XE1T.CTPC.BOARD09.CHAN008.VMON',
        'pmt_138_bias_V': 'XE1T.CTPC.BOARD09.CHAN009.VMON',
        'pmt_139_bias_V': 'XE1T.CTPC.BOARD09.CHAN010.VMON',
        'pmt_140_bias_V': 'XE1T.CTPC.BOARD11.CHAN002.VMON',
        'pmt_141_bias_V': 'XE1T.CTPC.BOARD11.CHAN003.VMON',
        'pmt_142_bias_V': 'XE1T.CTPC.BOARD11.CHAN004.VMON',
        'pmt_143_bias_V': 'XE1T.CTPC.BOARD09.CHAN011.VMON',
        'pmt_144_bias_V': 'XE1T.CTPC.BOARD09.CHAN012.VMON',
        'pmt_145_bias_V': 'XE1T.CTPC.BOARD09.CHAN013.VMON',
        'pmt_146_bias_V': 'XE1T.CTPC.BOARD09.CHAN014.VMON',
        'pmt_147_bias_V': 'XE1T.CTPC.BOARD09.CHAN015.VMON',
        'pmt_148_bias_V': 'XE1T.CTPC.BOARD08.CHAN021.VMON',
        'pmt_149_bias_V': 'XE1T.CTPC.BOARD11.CHAN005.VMON',
        'pmt_150_bias_V': 'XE1T.CTPC.BOARD11.CHAN006.VMON',
        'pmt_151_bias_V': 'XE1T.CTPC.BOARD11.CHAN007.VMON',
        'pmt_152_bias_V': 'XE1T.CTPC.BOARD11.CHAN008.VMON',
        'pmt_153_bias_V': 'XE1T.CTPC.BOARD09.CHAN016.VMON',
        'pmt_154_bias_V': 'XE1T.CTPC.BOARD09.CHAN017.VMON',
        'pmt_155_bias_V': 'XE1T.CTPC.BOARD09.CHAN018.VMON',
        'pmt_156_bias_V': 'XE1T.CTPC.BOARD09.CHAN019.VMON',
        'pmt_157_bias_V': 'XE1T.CTPC.BOARD10.CHAN000.VMON',
        'pmt_158_bias_V': 'XE1T.CTPC.BOARD10.CHAN001.VMON',
        'pmt_159_bias_V': 'XE1T.CTPC.BOARD11.CHAN009.VMON',
        'pmt_160_bias_V': 'XE1T.CTPC.BOARD11.CHAN010.VMON',
        'pmt_161_bias_V': 'XE1T.CTPC.BOARD11.CHAN011.VMON',
        'pmt_162_bias_V': 'XE1T.CTPC.BOARD11.CHAN012.VMON',
        'pmt_163_bias_V': 'XE1T.CTPC.BOARD11.CHAN013.VMON',
        'pmt_164_bias_V': 'XE1T.CTPC.BOARD09.CHAN020.VMON',
        'pmt_165_bias_V': 'XE1T.CTPC.BOARD09.CHAN021.VMON',
        'pmt_166_bias_V': 'XE1T.CTPC.BOARD09.CHAN022.VMON',
        'pmt_167_bias_V': 'XE1T.CTPC.BOARD10.CHAN002.VMON',
        'pmt_168_bias_V': 'XE1T.CTPC.BOARD10.CHAN003.VMON',
        'pmt_169_bias_V': 'XE1T.CTPC.BOARD10.CHAN004.VMON',
        'pmt_170_bias_V': 'XE1T.CTPC.BOARD11.CHAN014.VMON',
        'pmt_171_bias_V': 'XE1T.CTPC.BOARD11.CHAN015.VMON',
        'pmt_172_bias_V': 'XE1T.CTPC.BOARD11.CHAN016.VMON',
        'pmt_173_bias_V': 'XE1T.CTPC.BOARD11.CHAN017.VMON',
        'pmt_174_bias_V': 'XE1T.CTPC.BOARD11.CHAN018.VMON',
        'pmt_175_bias_V': 'XE1T.CTPC.BOARD11.CHAN019.VMON',
        'pmt_176_bias_V': 'XE1T.CTPC.BOARD09.CHAN023.VMON',
        'pmt_177_bias_V': 'XE1T.CTPC.BOARD10.CHAN005.VMON',
        'pmt_178_bias_V': 'XE1T.CTPC.BOARD10.CHAN006.VMON',
        'pmt_179_bias_V': 'XE1T.CTPC.BOARD10.CHAN007.VMON',
        'pmt_180_bias_V': 'XE1T.CTPC.BOARD10.CHAN008.VMON',
        'pmt_181_bias_V': 'XE1T.CTPC.BOARD10.CHAN009.VMON',
        'pmt_182_bias_V': 'XE1T.CTPC.BOARD11.CHAN020.VMON',
        'pmt_183_bias_V': 'XE1T.CTPC.BOARD11.CHAN021.VMON',
        'pmt_184_bias_V': 'XE1T.CTPC.BOARD13.CHAN000.VMON',
        'pmt_185_bias_V': 'XE1T.CTPC.BOARD13.CHAN001.VMON',
        'pmt_186_bias_V': 'XE1T.CTPC.BOARD13.CHAN002.VMON',
        'pmt_187_bias_V': 'XE1T.CTPC.BOARD11.CHAN022.VMON',
        'pmt_188_bias_V': 'XE1T.CTPC.BOARD10.CHAN010.VMON',
        'pmt_189_bias_V': 'XE1T.CTPC.BOARD10.CHAN011.VMON',
        'pmt_190_bias_V': 'XE1T.CTPC.BOARD10.CHAN012.VMON',
        'pmt_191_bias_V': 'XE1T.CTPC.BOARD10.CHAN013.VMON',
        'pmt_192_bias_V': 'XE1T.CTPC.BOARD10.CHAN014.VMON',
        'pmt_193_bias_V': 'XE1T.CTPC.BOARD11.CHAN023.VMON',
        'pmt_194_bias_V': 'XE1T.CTPC.BOARD13.CHAN003.VMON',
        'pmt_195_bias_V': 'XE1T.CTPC.BOARD13.CHAN004.VMON',
        'pmt_196_bias_V': 'XE1T.CTPC.BOARD13.CHAN005.VMON',
        'pmt_197_bias_V': 'XE1T.CTPC.BOARD13.CHAN006.VMON',
        'pmt_198_bias_V': 'XE1T.CTPC.BOARD13.CHAN007.VMON',
        'pmt_199_bias_V': 'XE1T.CTPC.BOARD12.CHAN000.VMON',
        'pmt_200_bias_V': 'XE1T.CTPC.BOARD12.CHAN001.VMON',
        'pmt_201_bias_V': 'XE1T.CTPC.BOARD10.CHAN015.VMON',
        'pmt_202_bias_V': 'XE1T.CTPC.BOARD10.CHAN016.VMON',
        'pmt_203_bias_V': 'XE1T.CTPC.BOARD10.CHAN017.VMON',
        'pmt_204_bias_V': 'XE1T.CTPC.BOARD10.CHAN018.VMON',
        'pmt_205_bias_V': 'XE1T.CTPC.BOARD13.CHAN008.VMON',
        'pmt_206_bias_V': 'XE1T.CTPC.BOARD13.CHAN009.VMON',
        'pmt_207_bias_V': 'XE1T.CTPC.BOARD13.CHAN010.VMON',
        'pmt_208_bias_V': 'XE1T.CTPC.BOARD13.CHAN011.VMON',
        'pmt_209_bias_V': 'XE1T.CTPC.BOARD13.CHAN012.VMON',
        'pmt_210_bias_V': 'XE1T.CTPC.BOARD12.CHAN002.VMON',
        'pmt_211_bias_V': 'XE1T.CTPC.BOARD12.CHAN003.VMON',
        'pmt_212_bias_V': 'XE1T.CTPC.BOARD12.CHAN004.VMON',
        'pmt_213_bias_V': 'XE1T.CTPC.BOARD10.CHAN019.VMON',
        'pmt_214_bias_V': 'XE1T.CTPC.BOARD10.CHAN020.VMON',
        'pmt_215_bias_V': 'XE1T.CTPC.BOARD10.CHAN021.VMON',
        'pmt_216_bias_V': 'XE1T.CTPC.BOARD13.CHAN013.VMON',
        'pmt_217_bias_V': 'XE1T.CTPC.BOARD13.CHAN014.VMON',
        'pmt_218_bias_V': 'XE1T.CTPC.BOARD13.CHAN015.VMON',
        'pmt_219_bias_V': 'XE1T.CTPC.BOARD13.CHAN016.VMON',
        'pmt_220_bias_V': 'XE1T.CTPC.BOARD12.CHAN005.VMON',
        'pmt_221_bias_V': 'XE1T.CTPC.BOARD12.CHAN006.VMON',
        'pmt_222_bias_V': 'XE1T.CTPC.BOARD12.CHAN007.VMON',
        'pmt_223_bias_V': 'XE1T.CTPC.BOARD12.CHAN008.VMON',
        'pmt_224_bias_V': 'XE1T.CTPC.BOARD10.CHAN022.VMON',
        'pmt_225_bias_V': 'XE1T.CTPC.BOARD10.CHAN023.VMON',
        'pmt_226_bias_V': 'XE1T.CTPC.BOARD13.CHAN017.VMON',
        'pmt_227_bias_V': 'XE1T.CTPC.BOARD13.CHAN018.VMON',
        'pmt_228_bias_V': 'XE1T.CTPC.BOARD13.CHAN019.VMON',
        'pmt_229_bias_V': 'XE1T.CTPC.BOARD12.CHAN009.VMON',
        'pmt_230_bias_V': 'XE1T.CTPC.BOARD12.CHAN010.VMON',
        'pmt_231_bias_V': 'XE1T.CTPC.BOARD12.CHAN011.VMON',
        'pmt_232_bias_V': 'XE1T.CTPC.BOARD12.CHAN012.VMON',
        'pmt_233_bias_V': 'XE1T.CTPC.BOARD12.CHAN013.VMON',
        'pmt_234_bias_V': 'XE1T.CTPC.BOARD12.CHAN014.VMON',
        'pmt_235_bias_V': 'XE1T.CTPC.BOARD13.CHAN020.VMON',
        'pmt_236_bias_V': 'XE1T.CTPC.BOARD13.CHAN021.VMON',
        'pmt_237_bias_V': 'XE1T.CTPC.BOARD13.CHAN022.VMON',
        'pmt_238_bias_V': 'XE1T.CTPC.BOARD12.CHAN015.VMON',
        'pmt_239_bias_V': 'XE1T.CTPC.BOARD12.CHAN016.VMON',
        'pmt_240_bias_V': 'XE1T.CTPC.BOARD12.CHAN017.VMON',
        'pmt_241_bias_V': 'XE1T.CTPC.BOARD12.CHAN018.VMON',
        'pmt_242_bias_V': 'XE1T.CTPC.BOARD12.CHAN019.VMON',
        'pmt_243_bias_V': 'XE1T.CTPC.BOARD13.CHAN023.VMON',
        'pmt_244_bias_V': 'XE1T.CTPC.BOARD12.CHAN020.VMON',
        'pmt_245_bias_V': 'XE1T.CTPC.BOARD12.CHAN021.VMON',
        'pmt_246_bias_V': 'XE1T.CTPC.BOARD12.CHAN022.VMON',
        'pmt_247_bias_V': 'XE1T.CTPC.BOARD12.CHAN023.VMON',
        'pmt_248_bias_V': 'XE1T.CTPC.BOARD08.CHAN015.VMON',
        'pmt_249_bias_V': 'XE1T.CTPC.BOARD08.CHAN016.VMON',
        'pmt_250_bias_V': 'XE1T.CTPC.BOARD08.CHAN017.VMON',
        'pmt_251_bias_V': 'XE1T.CTPC.BOARD08.CHAN018.VMON',
        'pmt_252_bias_V': 'XE1T.CTPC.BOARD08.CHAN019.VMON',
        'pmt_253_bias_V': 'XE1T.CTPC.BOARD08.CHAN020.VMON'
    }
}

# MongoDB settings
PASSWORD = os.environ.get("MONGO_PASSWORD")
CONNECTION = pymongo.MongoClient('mongodb://analyst:%s@'
                                 'zenigata.uchicago.edu:27020/'
                                 'slow_control' % PASSWORD)

COLLECTION = CONNECTION.slow_control.measurements


def get_value(variable, time_range=None,
              extension=datetime.timedelta(minutes=0)):
    query = {"name": variable}
    if time_range is not None:
        query['request_time'] = {'$gt': time_range[0] - extension,
                                 '$lt': time_range[1] + extension}

    return [(doc['request_time'], doc['value']) for doc in COLLECTION.find(query)]

def get_series(name, time_range=None):
    result = get_value(name, time_range=time_range)
    if len(result) == 0:
        return pd.Series()

    a,b = zip(*result)
    return pd.Series(b,a)

def get_dataframe(time_range=None):
    data = {}
    for name, category in VARIABLES.items():
        for key, value in category.items():
            data[key] = get_series(value,
                                   time_range)
    return pd.DataFrame(data)
