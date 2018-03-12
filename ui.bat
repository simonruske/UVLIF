@echo off
echo Producing python user interface files
call pyuic5 UVLIF/gui/main.ui -o UVLIF/gui/main_ui.py
call pyuic5 UVLIF/gui/analysis.ui -o UVLIF/gui/analysis_ui.py
call pyuic5 UVLIF/gui/configuration.ui -o UVLIF/gui/configuration_ui.py
call pyuic5 UVLIF/gui/filelist.ui -o UVLIF/gui/filelist_ui.py
call pyuic5 UVLIF/gui/analysis_configuration.ui -o UVLIF/gui/analysis_configuration_ui.py
echo Complete