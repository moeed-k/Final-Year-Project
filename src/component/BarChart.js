import React from 'react'
import {Bar} from 'react-chartjs-2';
import {Chart as Chart} from 'chart.js/auto';
import {useState} from 'react';
import PropTypes from 'prop-types';
export default function BarChart({chartData}) {
  
  return <Bar data={chartData}/>
  
}
