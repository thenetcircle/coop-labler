import Vue from 'vue'
import './plugins/vuetify'
import './plugins/vuetify'
import App from './App.vue'
import axios from 'axios'
import v4 from 'uuid'

Vue.config.productionTip = false

new Vue({
  render: (h) => h(App),
}).$mount('#app')

Vue.directive('canvas', {
  inserted(el) {
    const canvas = el as HTMLCanvasElement
    const ctx = canvas.getContext('2d')

    if (ctx === null) {
      return
    }

    canvas.width = 1000
    canvas.height = 800

    ctx.lineJoin = 'round'
    ctx.lineCap = 'round'
    ctx.lineWidth = 5

    let prevPos = {
      offsetX: 0,
      offsetY: 0,
    }

    let line: any[] = []
    let isPainting = false
    const userId = v4()
    const USER_STROKE = 'red'


    function handleMouseDown(e: any) {
      const {
        offsetX,
        offsetY,
      } = e
      prevPos = {
        offsetX,
        offsetY,
      }
      isPainting = true
    }


    function endPaintEvent() {
      if (isPainting) {
        isPainting = false
        sendPaintData()
      }
    }

    function handleMouseMove(e: any) {
      if (isPainting) {
        const {
          offsetX,
          offsetY,
        } = e

        const offSetData = {
          offsetX,
          offsetY,
        }

        const positionInfo = {
          start: {
            ...prevPos,
          },
          stop: {
            ...offSetData,
          },
        }
        line = line.concat(positionInfo)
        paint(prevPos, offSetData, USER_STROKE)
      }
    }

    function sendPaintData() {
      const body = {
        line,
        userId,
      }
      fetch('http://localhost:4000/paint', {
        method: 'post',
        body: JSON.stringify(body),
        headers: {
          'content-type': 'application/json',
        },
      }).then(() => (line = []))
    }

    function paint(
      prevPosition: any,
      currPosition: any,
      strokeStyle: string | CanvasGradient | CanvasPattern,
    ) {
      const {
        offsetX,
        offsetY,
      } = currPosition

      const {
        offsetX: x,
        offsetY: y,
      } = prevPosition

      if (ctx === null) {
        return
      }

      ctx.beginPath()
      ctx.strokeStyle = strokeStyle
      ctx.moveTo(x, y)
      ctx.lineTo(offsetX, offsetY)
      ctx.stroke()

      prevPos = {
        offsetX,
        offsetY,
      }
    }

    canvas.addEventListener('mousedown', handleMouseDown)
    canvas.addEventListener('mousemove', handleMouseMove)
    canvas.addEventListener('mouseup', endPaintEvent)
    canvas.addEventListener('mouseleave', endPaintEvent)
  },
})
