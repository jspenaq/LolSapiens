import { useState, useEffect } from 'react'
import iwiLogo from './assets/iwi.png'
import './App.css'

function App() {
  const [data, setData] = useState('IWICOSAS');

  useEffect(() => {
    async function getData(){
      const res = await fetch("http://127.0.0.1:8000/");
      const dataRes = await res.json();
      setData(dataRes);
    }
    getData();
    return () => {
      setData('')
    }
  }, [setData])
  


  return (
    <div className="App">
      <div>
        <img src="/vite.svg" className="logo" alt="Vite logo" />
        <img src={iwiLogo} className="logo react" alt="React logo" />
      </div>
      <h1>LoL Sapiens!</h1>
      <div className="card">
        <p>
          {JSON.stringify(data)}
        </p>
      </div>
    </div>
  )
}

export default App
