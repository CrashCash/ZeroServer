#! /usr/bin/env python3

import zero_server
from flask import Flask, render_template

# convert Celsius to Fahrenheit
def c2f(c):
   return (c*9/5)+32

def create_app(test_config=None):
   app=Flask(__name__, instance_relative_config=True)
   app.config.from_mapping (
      SECRET_KEY='dev',
   )

   @app.route("/")
   @app.route("/charging")
   def charging_status():
       pwpk=zero_server.read('PwPk')
       if isinstance(pwpk, str):
           return render_template('error.html', error=pwpk.capitalize())

       dst3=zero_server.read('DSt3')
       btst=zero_server.read('BtSt')

       t=dst3['minutes_until_charged']
       h, m=divmod(t, 60)

       warnings=[]
       if btst['battery_charge_critical_low']:
           warnings.append('Battery charge extremely low')
       if btst['battery_charge_low']:
           warnings.append('Battery charge low')
       if btst['battery_out_of_balance']:
           warnings.append('Battery out of balance')
       if btst['battery_temp_cold']:
           warnings.append('Battery cold')
       if btst['battery_temp_critical_high']:
           warnings.append('Battery extremely hot')
       if btst['battery_temp_high']:
           warnings.append('Battery hot')

       data={'time': pwpk['time'],
             'time_remaining': '%d:%02d' % (h, m),
             'min_temp': '%.1f' % (c2f(pwpk['pack_temp_min_c'])),
             'max_temp': '%.1f' % (c2f(pwpk['pack_temp_max_c'])),
             'voltage': '%.1f' % (pwpk['pack_voltage_mv']/1000),
             'cell_voltage_min': '%.3f' % (pwpk['cell_voltage_min_mv']/1000),
             'cell_voltage_max': '%.3f' % (pwpk['cell_voltage_max_mv']/1000),
             'imbalance': '%d' % (pwpk['cell_voltage_max_mv']-pwpk['cell_voltage_min_mv']),
             'cycles': '%d' % (pwpk['num_charge_cycles']),
             'percentage': '%d' % (pwpk['charge_pct']),
             'tot_kwh': '%d' % (btst['total_power_used_kw']),
             'avg_wh': '%.2f' % (dst3['wh_per_km_life']*1.609),
             'amps': '%d' % (-pwpk['battery_current_amps']),
             'watts': '%d' % ((-pwpk['battery_current_amps']*pwpk['pack_voltage_mv'])/1000),
             'warnings': warnings}

       return render_template('charging_status.html', **data)

   @app.route("/info")
   def info():
       gbki=zero_server.read('Gbki')
       if isinstance(gbki, str):
           return render_template('error.html', error=gbki.capitalize())

       btst=zero_server.read('BtSt')
       dst1=zero_server.read('DSt1')
       dst2=zero_server.read('DSt2')

       year=zero_server.zerobt.mbb_model[gbki['mbb_partno']]
       data={'name': year+' Zero '+gbki['model'],
             'vin': gbki['vin'],
             'odometer': format(btst['odometer_miles'], ',d'),
             'trip1': format(dst1['trip_1_km']/1.609, ',.01f'),
             'trip2': format(dst2['trip_2_km']/1.609, ',.01f')}

       return render_template('bike_info.html', **data)

   return app
