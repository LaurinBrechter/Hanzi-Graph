// import { useState } from 'react'
import './App.css'
import Graph from './components/graph/Graph'
import Info from './components/info/Info'
import Topbar from './components/topbar/Topbar'

function App() {

  return (
    <>
      <Topbar />
      <div className='main-container'>
        <Graph />
        <Info />
      </div>
      {/* <div>Hello</div> */}
    </>
  )
}

export default App
