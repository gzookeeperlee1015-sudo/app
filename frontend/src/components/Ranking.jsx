import { useEffect, useState } from 'react'

/**
 * 랭킹 컴포넌트
 * - 인트로 화면 오른쪽에 표시
 * - 백엔드에서 상위 20명 플레이어 데이터 가져와 표시
 */
function Ranking() {
  const [ranking, setRanking] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/game/ranking/')
      .then(res => res.json())
      .then(data => setRanking(data.ranking))
      .catch(err => console.error('랭킹 로딩 실패:', err))
      .finally(() => setLoading(false))
  }, [])

  // 숫자 포맷
  const fmt = (n) => Math.round(n).toLocaleString('ko-KR')

  return (
    <div className="bg-white rounded-[2rem] border border-slate-100 shadow-sm p-10 flex flex-col">
      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3 block">
        Ranking
      </span>
      <h2 className="text-xl font-black text-slate-900 mb-6">명예의 전당</h2>

      {loading ? (
        // 로딩 중
        <div className="flex-1 flex items-center justify-center">
          <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : ranking.length === 0 ? (
        // 아직 아무도 플레이 안 했을 때
        <div className="flex-1 flex items-center justify-center">
          <p className="text-slate-300 text-sm font-bold uppercase tracking-widest">
            아직 기록이 없어요
          </p>
        </div>
      ) : (
        // 랭킹 목록
        <div className="flex flex-col gap-3">
          {ranking.map((player) => (
            <div
              key={player.rank}
              className="flex items-center justify-between bg-slate-50 rounded-2xl px-4 py-3 border border-slate-100"
            >
              <div className="flex items-center gap-3">
                {/* 순위 */}
                <span className={`text-sm font-black w-6 text-center
                  ${player.rank === 1 ? 'text-yellow-400' :
                    player.rank === 2 ? 'text-slate-400' :
                    player.rank === 3 ? 'text-amber-600' : 'text-slate-300'}`}
                >
                  {player.rank}
                </span>
                {/* 닉네임 */}
                <p className="text-sm font-black text-slate-800">{player.nickname}</p>
              </div>

              {/* 자산만 표시 */}
              <p className="text-sm font-black text-slate-800">{fmt(player.balance)}원</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Ranking
