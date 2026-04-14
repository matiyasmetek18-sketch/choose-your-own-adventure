import { useState } from 'react'
import { useStory } from './hooks/useStory'
import StoryReader from './components/StoryReader'
import StoryGraph from './components/StoryGraph'
import './App.css'

export default function App() {
  const { page, currentPage, history, goToPage, goBack, restart, allPages } = useStory()
  const [showGraph, setShowGraph] = useState(true)

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-left">
          <span className="app-logo">🕳️</span>
          <h1 className="app-title">The Cave of Time</h1>
          <span className="app-subtitle">Choose Your Own Adventure</span>
        </div>
        <div className="header-right">
          <button
            className={`btn btn-toggle ${showGraph ? 'active' : ''}`}
            onClick={() => setShowGraph(g => !g)}
          >
            {showGraph ? '🗺️ Hide Map' : '🗺️ Show Map'}
          </button>
        </div>
      </header>

      <main className={`app-main ${showGraph ? 'with-graph' : 'no-graph'}`}>
        <div className="reader-panel">
          <StoryReader
            page={page}
            history={history}
            onChoice={goToPage}
            onBack={goBack}
            onRestart={restart}
          />
        </div>

        {showGraph && (
          <div className="graph-panel">
            <div className="graph-title">Story Map</div>
            <StoryGraph
              allPages={allPages}
              currentPage={currentPage}
              onNodeClick={goToPage}
            />
          </div>
        )}
      </main>
    </div>
  )
}