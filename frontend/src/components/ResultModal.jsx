/**
 * 게임 결과 모달 컴포넌트
 * - 게임 종료 또는 처음으로 돌아갈 때 표시
 * - 이번 게임 수익/손실 및 누적 자산 표시
 */
function ResultModal({ profit, totalAsset, onClose, isBankrupt = false }) {
  const fmt = (n) => Math.round(n).toLocaleString('ko-KR')

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-[2rem] border border-slate-100 shadow-xl p-10 w-full max-w-sm mx-4 text-center">

        {isBankrupt ? (
          <>
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Game Over</p>
            <p className="text-3xl font-black text-slate-900 mb-2">파산!</p>
            <p className="text-sm text-slate-400 mb-6">자산이 200원 이하로 떨어졌어요</p>
            <p className="text-sm font-black text-blue-500 mb-8">자본금 1,000만원으로 초기화됐어요</p>
          </>
        ) : (
          <>
            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Result</p>
            <p className="text-xl font-black text-slate-900 mb-6">게임 결과</p>

            {/* 이번 게임 수익 */}
            <div className="bg-slate-50 rounded-2xl p-5 mb-4 border border-slate-100">
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">이번 게임 수익</p>
              <p className={`text-3xl font-black ${profit >= 0 ? 'text-red-500' : 'text-blue-500'}`}>
                {profit >= 0 ? '+' : ''}{fmt(profit)}원
              </p>
            </div>

            {/* 누적 자산 */}
            <div className="bg-slate-50 rounded-2xl p-5 mb-8 border border-slate-100">
              <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">누적 자산</p>
              <p className="text-2xl font-black text-slate-900">{fmt(totalAsset)}원</p>
            </div>
          </>
        )}

        {/* 확인 버튼 */}
        <button
          onClick={onClose}
          className="w-full bg-slate-900 hover:bg-blue-600 text-white font-black py-3 rounded-xl text-sm uppercase tracking-widest transition-all"
        >
          확인
        </button>

      </div>
    </div>
  )
}

export default ResultModal
