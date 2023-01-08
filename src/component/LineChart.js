import React from 'react'
import {Line} from 'react-chartjs-2';
import {Chart as Chart} from 'chart.js/auto';
import {useState} from 'react';
import PropTypes from 'prop-types';
export default function LineChart({chartData}) {
  
  return <Line data={chartData}/>
  
}
