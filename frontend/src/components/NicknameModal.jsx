import { useState } from 'react'

/**
 * 닉네임 입력 모달 컴포넌트
 * - 게임 최초 진입 시 표시
 * - 닉네임 입력 후 백엔드에서 플레이어 정보(자산) 가져옴
 * - 기존 플레이어면 이전 자산 그대로, 신규면 1000만원으로 시작
 */
function NicknameModal({ onConfirm }) {
  const [nickname, setNickname] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    const trimmed = nickname.trim()
    if (!trimmed) {
      setError('닉네임을 입력해주세요.')
      return
    }
    if (trimmed.length > 20) {
      setError('닉네임은 20자 이하로 입력해주세요.')
      return
    }

    setLoading(true)
    setError('')

    try {
      // 닉네임으로 로그인 또는 신규 생성
      const res = await fetch('http://127.0.0.1:8000/api/game/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nickname: trimmed }),
      })
      const data = await res.json()

      if (!res.ok) {
        setError(data.error || '오류가 발생했습니다.')
        return
      }

      // 부모(StockGame)에 닉네임과 자산 전달
      onConfirm({
        nickname: data.nickname,
        balance: data.balance,
        isNew: data.is_new,
      })
    } catch (err) {
      setError('서버 연결에 실패했습니다.')
    } finally {
      setLoading(false)
    }
  }

  return (
    // 모달 배경 오버레이
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-[2rem] border border-slate-100 shadow-xl p-10 w-full max-w-md mx-4">

        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 block">
          Player
        </span>
        <h2 className="text-2xl font-black text-slate-900 mb-2">닉네임을 입력하세요</h2>
        <p className="text-sm text-slate-400 mb-8">
          기존 닉네임 입력 시 이전 자산을 그대로 이어받아요
        </p>

        {/* 닉네임 입력 */}
        <input
          type="text"
          placeholder="닉네임 입력 (최대 20자)"
          value={nickname}
          onChange={e => setNickname(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSubmit()}
          maxLength={20}
          className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-blue-400 mb-3"
        />

        {/* 에러 메시지 */}
        {error && (
          <p className="text-red-400 text-xs font-bold mb-3">{error}</p>
        )}

        {/* 확인 버튼 */}
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-slate-900 hover:bg-blue-600 text-white font-black py-3 rounded-xl text-sm uppercase tracking-widest transition-all disabled:opacity-40"
        >
          {loading ? '확인 중...' : '시작하기'}
        </button>

      </div>
    </div>
  )
}

export default NicknameModal
