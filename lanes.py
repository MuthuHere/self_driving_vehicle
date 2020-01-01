from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean
import numpy as np

def draw_lanes(img, lines, color=[0,255,255], thickness=3):
    #if no lines found
    try:
        ys = []
        for line in lines:
            for xy in line:
                ys += [xy[1],xy[3]]
        min_y = min(ys)
        max_y = 600 #horizon

        line_dict = {}

        for id,line in enumerate(lines):
            for xy in line:
                x_coords = (xy[0], xy[2])
                y_coords = (xy[1], xy[3])
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(a, y_coords)[0]

                #improved x calculation
                x1 = (min_y-b)/m
                x2 = (max_y-b)/m

                line_dict[id] = [m,b,[int(x1),min_y,int(x2),max_y]]

        final_lanes = {}
        for id in line_dict:
            final_lanes_copy = final_lanes.copy()
            m = line_dict[id][0]
            b = line_dict[id][1]
            line = line_dict[id][2]
            if len(final_lanes) == 0:
                final_lanes[m] = [[m, b, line]]
            else:
                found_copy = false
                for other_ms in final_lanes_copy:
                    if not found_copy:
                        if abs(other_ms*1.2)>abs(m)>abs(other_ms*0.8):
                            if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                                final_lanes[other_ms].append([m,b,line])
                                found_copy = True
                                break
                        else:
                            final_lanes[m] = [ [m,b,line] ]

        line_counter = {}

        for lanes in final_lanes:
            line_counter[lanes] = len(final_lanes[lanes])

        top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        lane1_id = top_lanes[0][0]
        lane2_id = top_lanes[1][0]

        def average_lane(lane_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in lane_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(mean(x1s)), int(mean(y1s)), int(mean(x2s)), int(mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_lane(final_lanes[lane1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_lane(final_lanes[lane2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], lane1_id, lane2_id
    except Exception as e:
        print(str(e))
