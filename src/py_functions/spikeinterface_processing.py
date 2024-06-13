import numpy as np
import os
import pandas as pd
import spikeinterface.full as si 
from typing import Tuple, List
from probeinterface import Probe

### TODO: RELLENAR CON DOCSTRINGS!!
### TODO: JUNTAR load_recording_from_raw / load_recording_from_raw_independent_channels


def load_recording_from_raw(root: str, sample_base: str, well: Tuple[int, int], time_samplings_to_mask: List[Tuple[float, float]]):

    traces_list = []
    channel_ids = []

    df = pd.read_csv(f'{root}/{sample_base}/{sample_base}.info', index_col=0, names=['index', 'value'], sep='\t')
    sampling_frequency = df.loc['SamplingFrequency', 'value']
    voltage_scale = np.abs(df.loc['VoltageScale', 'value'])

    # We choose 10 here because in 64-electrode MEAs the range would be up to 9. 
    # Since the time required for the non-existing electrodes is small, we don't mine using a larger number.
    for Erow in range(1,10):  
        for Ecol in range(1,10):
            filename = f'{root}/{sample_base}/{well[0]}-{well[1]}-{Erow}-{Ecol}_voltageRaw'
            is_txt, is_gzip = os.path.exists(f'{filename}.txt'), os.path.exists(f'{filename}.txt.gz') 

            if is_txt or is_gzip:
                channel_ids.append(f'{Erow}-{Ecol}')
                
                if is_txt:
                    list_voltages = np.loadtxt(f'{filename}.txt')
                elif is_gzip:
                    list_voltages = np.loadtxt(f'{filename}.txt.gz')

                traces_list.append(list_voltages)
            

    trace_array = np.asarray(traces_list).transpose() / voltage_scale

    for time_sampling in time_samplings_to_mask:
        t0 = int(time_sampling[0] * sampling_frequency)
        tf = int(time_sampling[1] * sampling_frequency)
        trace_array[t0:tf, :] = 0

    sample_recording = si.NumpyRecording(
        traces_list=[trace_array],
        sampling_frequency=sampling_frequency,
        channel_ids=np.asarray(channel_ids)
    )

    sample_recording.set_property('group', [0] * len(channel_ids))
    sample_recording.is_dumpable = True  # This is necessary for some options later, like spike sorting

    return sample_recording





def load_recording_from_raw_independent_channels(root: str, 
                                                 sample_base: str, 
                                                 well: Tuple[int, int], 
                                                 time_samplings_to_mask: List[Tuple[float, float]]):
    dict_recordings = {}

    traces_list = []
    channel_ids = []

    df = pd.read_csv(f'{root}/{sample_base}/{sample_base}.info', index_col=0, names=['index', 'value'], sep='\t')
    sampling_frequency = df.loc['SamplingFrequency', 'value']
    voltage_scale = np.abs(df.loc['VoltageScale', 'value'])

    # We choose 10 here because in 64-electrode MEAs the range would be up to 9. 
    # Since the time required for the non-existing electrodes is small, we don't mine using a larger number.
    for Erow in range(1,10):  
        for Ecol in range(1,10):
            filename = f'{root}/{sample_base}/{well[0]}-{well[1]}-{Erow}-{Ecol}_voltageRaw'
            is_txt, is_gzip = os.path.exists(f'{filename}.txt'), os.path.exists(f'{filename}.txt.gz') 

            if is_txt or is_gzip:
                channel_ids.append(f'{Erow}-{Ecol}')
                
                if is_txt:
                    list_voltages = np.loadtxt(f'{filename}.txt')
                elif is_gzip:
                    list_voltages = np.loadtxt(f'{filename}.txt.gz')

                traces_list.append(list_voltages)
            

    trace_array = np.asarray(traces_list).transpose() / voltage_scale

    for time_sampling in time_samplings_to_mask:
        t0 = int(time_sampling[0] * sampling_frequency)
        tf = int(time_sampling[1] * sampling_frequency)
        trace_array[t0:tf, :] = 0


    for idx in range(len(channel_ids)):
        sample_recording = si.NumpyRecording(
        traces_list=[trace_array[:, idx].reshape((-1, 1))],
        sampling_frequency=sampling_frequency,
        channel_ids=np.asarray([channel_ids[idx]]))

        sample_recording.set_property('group', [0] )
        sample_recording.is_dumpable = True  # This is necessary for some options later, like spike sorting

        dict_recordings[channel_ids[idx]] = {'base_recording': sample_recording}
    

    return dict_recordings




def load_probe_recording(recording: si.NumpyRecording, type_MEAS: int, ):
    dist_multiplier = 350 if type_MEAS == 16 else 300
    circle_radius = 50

    channel_ids = recording.get_channel_ids()

    positions = np.zeros((len(channel_ids), 2), dtype=float)
    contact_vector = []
    for channel_idx, channel in enumerate(channel_ids):
        x_coord, y_coord = (int(channel.split('-')[0]) - 1) * dist_multiplier, (int(channel.split('-')[1]) - 1) * dist_multiplier
        positions[channel_idx, 1], positions[channel_idx, 0] = x_coord, y_coord
        
        contact_vector.append((0, x_coord,   y_coord, 'circle', circle_radius, '', '', channel_idx, 'um', 1., 0., 0., 1.))

    # later if we are using peak detection, we may need it
    recording.set_channel_locations(locations=positions)

    probe = Probe(ndim=2, si_units='um')
    probe.set_contacts(positions=positions, shapes='circle', shape_params={'radius': circle_radius})
    probe.device_channel_indices = np.arange(len(channel_ids))
    probe.create_auto_shape('rect')

    recording.set_probe(probe)


    # Create contact_vector
    dtypes=[('probe_index', '<i8'), ('x', '<f8'), ('y', '<f8'), ('contact_shapes', '<U64'), 
            ('radius', '<f8'), ('shank_ids', '<U64'), ('contact_ids', '<U64'), ('device_channel_indices', '<i8'), 
            ('si_units', '<U64'), ('plane_axis_x_0', '<f8'), ('plane_axis_x_1', '<f8'), ('plane_axis_y_0', '<f8'), 
            ('plane_axis_y_1', '<f8')]

    recording.set_property('contact_vector', np.asarray(contact_vector, dtype=dtypes))


def recording_preprocessing(recording: si.NumpyRecording):
    ...
