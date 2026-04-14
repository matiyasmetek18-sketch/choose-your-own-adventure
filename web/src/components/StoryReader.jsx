export default function StoryReader({ page, history, onChoice, onBack, onRestart }) {
  if (!page) return <div className="reader-error">Page not found.</div>

  return (
    <div className="reader">
      <div className="reader-header">
        <span className="page-badge">Page {page.id}</span>
        <div className="reader-nav">
          {history.length > 1 && (
            <button className="btn btn-ghost" onClick={onBack}>← Back</button>
          )}
          <button className="btn btn-ghost" onClick={onRestart}>↩ Restart</button>
        </div>
      </div>

      <div className="story-text">
        {page.text.split('\n').filter(l => l.trim()).map((para, i) => (
          <p key={i}>{para}</p>
        ))}
      </div>

      <div className="choices">
        {page.isTerminal ? (
          <div className="ending">
            <div className="ending-title">— THE END —</div>
            <p className="ending-sub">You reached one of {52} possible endings.</p>
            <button className="btn btn-primary" onClick={onRestart}>Play Again</button>
          </div>
        ) : (
          page.choices.map((choice, i) => (
            <button
              key={i}
              className={`btn btn-choice ${page.isContinuation ? 'btn-continue' : ''}`}
              onClick={() => onChoice(choice.page)}
            >
              {page.isContinuation ? '▶ Continue reading...' : choice.text}
            </button>
          ))
        )}
      </div>

      <div className="breadcrumb">
        <span className="breadcrumb-label">Your path: </span>
        {history.map((p, i) => (
          <span key={i} className="breadcrumb-step">
            {i > 0 && <span className="breadcrumb-arrow">→</span>}
            <span className={p === history[history.length - 1] ? 'breadcrumb-current' : 'breadcrumb-past'}>
              {p}
            </span>
          </span>
        ))}
      </div>
    </div>
  )
}