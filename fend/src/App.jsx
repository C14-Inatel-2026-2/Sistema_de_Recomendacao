import { useState } from 'react';
import './App.css';
import Usuarios from './components/Usuarios';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
        <header className="App-header">
            <h1>Sistema de Recomendação</h1>
        </header>
        <main>
            <Usuarios/>
        </main>
    </div>
  )
}

export default App
