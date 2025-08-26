<template>
  <svg version="1.1" id="svg1" viewBox="0 0 688 86.666664"
    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd" xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg">
    <g inkscape:groupmode="layer" inkscape:label="Image" id="g1">
      <image width="688" height="86.666664" preserveAspectRatio="none" xlink:href="/assets/SurahHeader.png" />
      <text xml:space="preserve"
        style="text-align:start;writing-mode:lr-tb;direction:ltr;white-space:pre;shape-inside:url(#rect12114);display:inline;stroke:#00ff00;stroke-width:1.51937" />
      <text xml:space="preserve" :style="{ fill: isDark ? '#000' : '#fff' }"
        style="font-size:42.6667px;text-align:center;writing-mode:lr-tb;direction:ltr;text-anchor:start;stroke:none;stroke-width:1.51937"
        x="262.14975" y="58.382698">
        <tspan sodipodi:role="line" class="SurahNameSVG" x="350" y="58.382698" style="font-size:42.6667px;stroke:none;"
          text-anchor="middle" :style="{ fontFamily: fontFamily, fill: isDark ? '#000' : '#fff' }"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"> {{ SurahName }}
        </tspan>
      </text>
      <text xml:space="preserve"
        style="font-size:18.6667px;text-align:start;writing-mode:lr-tb;direction:ltr;text-anchor:start;stroke:none;stroke-width:1.51937"
        x="532.20746" y="42.124683" id="text12116-5">
        <tspan sodipodi:role="line" id="tspan12116-5" x="532.20746" y="42.124683"
          style="font-size:18.6667px;stroke:none;" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
          :style="{ fontFamily: fontFamily, fill: isDark ? '#000' : '#fff' }">صفحة</tspan>
      </text>
      <text xml:space="preserve"
        style="font-size:18.6667px;text-align:center;writing-mode:lr-tb;direction:ltr;text-anchor:start;stroke:none;stroke-width:1.51937"
        x="533.45758" y="58.382694">
        <tspan sodipodi:role="line" class="PageNumberSVG" x="550" y="58.382694" style="font-size:18.6667px;"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
          :style="{ fontFamily: fontFamily, fill: isDark ? '#000' : '#fff' }" text-anchor="middle">{{
            pageNumber }}</tspan>
      </text>
      <text xml:space="preserve"
        style="font-size:18.6667px;text-align:start;writing-mode:lr-tb;direction:ltr;text-anchor:start;stroke:none;stroke-width:1.51937"
        x="125.27171" y="38.699997" id="text12116-5-5">
        <tspan sodipodi:role="line" x="125.27171" y="38.699997" style="font-size:18.6667px;stroke:none;"
          :style="{ fontFamily: fontFamily, fill: isDark ? '#000' : '#fff' }"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">جزء</tspan>
      </text>
      <text xml:space="preserve"
        style="font-size:18.6667px;text-align:center;writing-mode:lr-tb;direction:ltr;text-anchor:start;stroke:none;stroke-width:1.51937"
        x="125.95278" y="58.106087">
        <tspan sodipodi:role="line" class="JuzNumberSVG" x="136" y="58.106087" style="font-size:18.6667px;"
          :style="{ fontFamily: fontFamily, fill: isDark ? '#000' : '#fff' }"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" text-anchor="middle">{{
            JuzNumber }}</tspan>
      </text>
    </g>
  </svg>

</template>

<script>
export default {
  name: "SurahInfo",
  props: {
    SurahName: {
      type: String,
      required: true,
    },
    pageNumber: {
      type: [String, Number],
      required: true,
    },
    JuzNumber: {
      type: [String, Number],
      required: true,
    },
    fontFamily: {
      type: String,
      required: true,
    },
    isDark: {
      type: Boolean,
      required: true,
    },
  },
}
</script>
