function [] = saveRawData(AllRawData, ROOT, SAVE_FOLDER, CRow, CCol, ERow, ECol)
    filename = returnFilename(ROOT, SAVE_FOLDER, CRow, CCol, ERow, ECol);

    % GET ELECTRODE INFO FROM RAW
    ElectrodeRawData = AllRawData{CRow, CCol, ERow, ECol};


    % Escribir esta información
    fid = fopen(strcat(ROOT, '\', SAVE_FOLDER, '\', SAVE_FOLDER, '.info'), 'w' ); %// open file to writing
    fprintf( fid, '%s',  sprintf(strcat('SamplingFrequency\t', ...
        num2str(ElectrodeRawData.Source.SamplingFrequency))));
    fprintf( fid, '%s',  sprintf(strcat('\nVoltageScale\t', ...
        num2str(ElectrodeRawData.Source.VoltageScale))));
    fprintf( fid, '%s',  sprintf(strcat('\nDuration\t', ...
        num2str(ElectrodeRawData.Source.Duration))));
    fclose( fid );


    timeRaw = ElectrodeRawData.GetTimeVector;
    filenameTimeRaw=strcat(filename, '_timeRaw.txt');
    writematrix(timeRaw, filenameTimeRaw);
    
    voltageRaw = ElectrodeRawData.GetVoltageVector;
    filenamevoltageRaw=strcat(filename, '_voltageRaw.txt');
    writematrix(voltageRaw, filenamevoltageRaw);
end

