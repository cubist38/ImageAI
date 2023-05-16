import torch
import numpy as np
import cv2
import os
from os import path as osp
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "pytracking"))
from pytracking.lib.test.evaluation import Tracker

def vis_traj(seq, output_boxes):
    frames_list = []
    for frame, box in zip(seq.frames, output_boxes):
        frame = cv2.imread(frame)
        x, y, w, h = box
        x1, y1, x2, y2 = map(lambda x: int(x), [x, y, (x + w), (y+h)])
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)
        frames_list.append(frame)
    return frames_list

def build_ostrack_model(tracker_param):
    tracker = Tracker('ostrack', tracker_param, "inpaint-videos")
    return tracker

def get_box_using_ostrack(tracker, seq, output_dir=None):
    output = tracker.run_sequence(seq, debug=False)
    tracked_bb = np.array(output['target_bbox']).astype(int)
    return tracked_bb