#!/bin/bash
echo 'parsing monthly average temperatures for Portugal...';
curl -s http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/portugal-TAVG-Trend.txt \
  | egrep "^% Estimated Jan(.*)+monthly" -A 2 \
  | tail -n 1 | tr -d "%" | tr -s '[:blank:]' \
  | cut -c 2- \
  | tr ' ' '\n' \
  > portugal_monthly_avg.csv;
echo 'parsing monthly historic temperature anomalies for Portugal...';
curl -s http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/portugal-TAVG-Trend.txt \
  | egrep -v "^%|^( )?$" \
  | tr -s '[:blank:]' \
  | cut -c 2- \
  | cut -d ' ' -f 1,2,3 \
  | tr ' ' ',' \
  > portugal_monthly_anom.csv;
echo 'parsing monthly average temperatures worldwide...';
curl -s http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/global-land-TAVG-Trend.txt \
  | egrep "^% Estimated Jan(.*)+monthly" -A 2 \
  | tail -n 1 | tr -d "%" | tr -s '[:blank:]' \
  | cut -c 2- \
  | tr ' ' '\n' \
  > world_monthly_avg.csv;
echo 'parsing monthly historic temperature anomalies worldwide...';
curl -s http://berkeleyearth.lbl.gov/auto/Regional/TAVG/Text/global-land-TAVG-Trend.txt \
  | egrep -v "^%|^( )?$" \
  | tr -s '[:blank:]' \
  | cut -c 2- \
  | cut -d ' ' -f 1,2,3 \
  | tr ' ' ',' \
  > world_monthly_anom.csv;

  