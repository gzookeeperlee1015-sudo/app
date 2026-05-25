import { useEffect, useRef, useImperativeHandle, forwardRef } from 'react'
import { createChart, CandlestickSeries } from 'lightweight-charts'

// forwardRef: 부모(StockGame)에서 차트에 캔들 추가하는 함수를 직접 호출하기 위해 사용
const CandleChart = forwardRef(({ data }, ref) => {
  const chartContainerRef = useRef(null)
  const chartRef = useRef(null)
  const candleSeriesRef = useRef(null)

  // 부모에서 호출 가능한 함수 노출
  useImperativeHandle(ref, () => ({
    // 캔들 한 개 추가
    addCandle(candle) {
      if (!candleSeriesRef.current) return
      candleSeriesRef.current.update({
        time: candle.date,
        open: candle.open,
        high: candle.high,
        low: candle.low,
        close: candle.close,
      })
    }
  }))

  useEffect(() => {
    if (!chartContainerRef.current || !data) return

    if (chartRef.current) {
      chartRef.current.remove()
    }

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#64748b',
      },
      grid: {
        vertLines: { color: '#f1f5f9' },
        horzLines: { color: '#f1f5f9' },
      },
      timeScale: {
        borderColor: '#e2e8f0',
        timeVisible: true,
      },
    })

    chartRef.current = chart

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#ef4444',
      downColor: '#3b82f6',
      borderUpColor: '#ef4444',
      borderDownColor: '#3b82f6',
      wickUpColor: '#ef4444',
      wickDownColor: '#3b82f6',
    })

    candleSeriesRef.current = candleSeries

    const formattedData = data.map(d => ({
      time: d.date,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    }))

    candleSeries.setData(formattedData)
    chart.timeScale().fitContent()

    const handleResize = () => {
      chart.applyOptions({ width: chartContainerRef.current.clientWidth })
    }
    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [data])

  return (
    <div className="rounded-xl overflow-hidden border border-slate-100">
      <div ref={chartContainerRef} />
    </div>
  )
})

export default CandleChart
