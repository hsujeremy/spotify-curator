import React from 'react';
import { render } from 'react-dom';
import App from './components/App';
import Home from './pages/Home'
import './App.css'


render(
    <Home />,
    document.getElementById('root')
);