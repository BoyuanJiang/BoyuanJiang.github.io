---
layout: page
permalink: /publications/
title: publications
description:  Boyuan Jiang's publications. * indicates equal contribution.
years: [2022, 2021, 2020, 2019, 2018]
nav: true
---
<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>

<div class="clustrmaps">
  <script type="text/javascript" id="clustrmaps" src="//clustrmaps.com/map_v2.js?d=EjRGPh2Dr65dqTqraYvkUlCl05O1zHSXvOMxpN_2rkQ&cl=ffffff&w=a"></script>
</div>