addpath('Z:\Nanoneuro\axion_matlab_files');

ROOT = 'Z:\Nanoneuro\data\results_dias_12-14';
FILENAME_BASIS = 'D12(000)(000)';


ROOT = 'Z:\Nanoneuro\data\rCxNs';
FILENAME_BASIS = 'p2.+-1000mV.500us(000)';

mkdir(ROOT, FILENAME_BASIS)

% LOAD ALL RAW AND SPIKE DATA
try
    FileDataRaw=AxisFile(strcat(ROOT, '\', FILENAME_BASIS, '.raw'));
    AllRawData=FileDataRaw.RawVoltageData.LoadData;
catch
    AllRawData = false;
end

try
    FileDataSpk=AxisFile(strcat(ROOT, '\', FILENAME_BASIS, '.spk'));
    AllSpikeData=FileDataSpk.SpikeData.LoadData;
catch
    AllSpikeData = false;
end



for CRow = 2:2  %1:4
    for CCol = 3:3 %1:4
        for ERow = 1:4
            for ECol = 1:4
               if not(isequal(AllRawData, false));
                    try
                        saveRawData(AllRawData, ROOT, FILENAME_BASIS, CRow, CCol, ERow, ECol);
                    catch
                        warning(strcat('Problem saving RAW data from Channel (', ...
                            num2str(CRow), ', ', num2str(CCol), ...
                            ') Electrode (', ...
                            num2str(ERow), ', ', num2str(ECol), ...
                            ')'))
                    end
                end
                
                if not(isequal(AllSpikeData, false));
                    try
                        saveSpkData(AllSpikeData, ROOT, FILENAME_BASIS, CRow, CCol, ERow, ECol);
                    catch
                        warning(strcat('Problem saving SPK data from Channel (', ...
                            num2str(CRow), ', ', num2str(CCol), ...
                            ') Electrode (', ...
                            num2str(ERow), ', ', num2str(ECol), ...
                            ')'))
                    end
                end
          
            end
        end
    end
end