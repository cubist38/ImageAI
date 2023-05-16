import os
from pytracking.lib.test.utils import TrackerParams
from pytracking.lib.config.ostrack.config import cfg, update_config_from_file


def parameters(yaml_name: str):
    params = TrackerParams()
    update_config_from_file('/content/FinalProject/pytracking/lib/config/ostrack/vitb_384_mae_ce_32x4_ep300.yaml'))
    params.cfg = cfg
    # print("test config: ", cfg)

    # template and search region
    params.template_factor = cfg.TEST.TEMPLATE_FACTOR
    params.template_size = cfg.TEST.TEMPLATE_SIZE
    params.search_factor = cfg.TEST.SEARCH_FACTOR
    params.search_size = cfg.TEST.SEARCH_SIZE

    # Network checkpoint path
    # params.checkpoint = os.path.join(save_dir, "checkpoints/train/ostrack/%s/OSTrack_ep%04d.pth.tar" %
    #                                  (yaml_name, cfg.TEST.EPOCH))
    params.checkpoint = os.path.join('/content/drive/MyDrive/vitb_384/mae_ce_32x4_ep300.pth')
    assert os.path.exists(params.checkpoint), f'checkpoint not found at {params.checkpoint}'

    # whether to save boxes from all queries
    params.save_all_boxes = False

    return params
