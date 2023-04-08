  lightTeal = "#afd0d3", midTeal = "#74adb7", darkTeal = "#3f8faa", logoBlue = "#097eb9", //blues
    yellow = "#f9dca7", yellowOrange = "#FFA45C", orange = "#ff7d62", brightOrange = "#F8715C", lightRed = "#c45353", darkRed = "#a03743", //oranges
    lightBrown = "#2d1c0d", medBrown = "#211308", darkBrown = "#160b04", beige = "#d8dbd2", offWhite = "#efefef", white = "#ffffff", //browns 
    twos = "#222222", threes = "#333333", fours = "#444444", fives = "#555555", sevens = "#777777", nines = "#999999", as = "#aaaaaa",
    $gears = $('#left-gear, #right-gear'),
    $conveyerTop = $('#belt-top'),
    $conveyerBottom = $('#belt-bottom'),
    $searchIn = $('#search-in'), $designIn = $('#design-in'), $inboundIn = $('#inbound-in'),
    $searchOut = $('#search-out'), $designOut = $('#design-out'), $inboundOut = $('#inbound-out'),
    $machine1 = $('#machine-1'), $machine2 = $('#machine-2'), $machine3 = $('#machine-3'), $machine4 = $('#machine-4'), $machine5 = $('#machine-5'),
    path0 = [{
      x: 0,
      y: 0
    }, {
      x: 50,
      y: 40
    }, {
      x: 60,
      y: 160
    }], path10 = [{
      x: 0,
      y: 0
    }, {
      x: 0,
      y: 10
    }, {
      x: 0,
      y: 170
    }], path1 = [{
      x: 0,
      y: 0
    }, {
      x: 30,
      y: 60
    }, {
      x: 45,
      y: 160
    }], path2 = [{
      x: 0,
      y: 0
    }, {
      x: 5,
      y: 20
    }, {
      x: 15,
      y: 170
    }], path3 = [{
      x: 0,
      y: 0
    }, {
      x: -25,
      y: 10
    }, {
      x: -35,
      y: 170
    }], path4 = [{
      x: 0,
      y: 0
    }, {
      x: -65,
      y: 10
    }, {
      x: -70,
      y: 170
    }], path5 = [{
      x: 0,
      y: 0
    }, {
      x: -85,
      y: 10
    }, {
      x: -105,
      y: 170
    }], path6 = [{
      x: 0,
      y: 0
    }, {
      x: -105,
      y: 30
    }, {
      x: -135,
      y: 160
    }], $postIt1 = $('#post-it-1'), $postIt2 = $('#post-it-2'), $postIt3 = $('#post-it-3'), $postIt4 = $('#post-it-4'), $postIt5 = $('#post-it-5'), $postIt6 = $('#post-it-6'), $glasses = $('#glasses-post-it'), $postIt7 = $('#post-it-7'), $postIt8 = $('#post-it-8'), $postIt9 = $('#post-it-9'), $postIt10 = $('#post-it-10'), $pen1 = $('#pen-1'), $pen2 = $('#pen-2'), $pen3 = $('#pen-3'), $pen4 = $('#pen-4'), $pen5 = $('#pen-5'), $pen6 = $('#pen-6'), $pen7 = $('#pen-7'), $pen8 = $('#pen-8'), $pen9 = $('#pen-9'),
    $material1 = $('#material-1'), $material2 = $('#material-2'), $material3 = $('#material-3'), $material4 = $('#material-4'), $material5 = $('#material-5'), $material6 = $('#material-6'), $pushable = $('#pushable'), $compressor1 = $('#compressor-1'), $compressor2 = $('#compressor-2'), $lever = $('#lever'), $bar1 = $('#bar-3'), $bar2 = $('#bar-4'), $bar3 = $('#bar-2'), $bar4 = $('#bar-1'),
    $needle = $('#machine-3-needle'), $sliderButtons = $('.square-slider-buttons'), $lightSequence = $('.light-sequence'), $machine3Light1 = $('#machine-3-light-1'), $machine3Light2 = $('#machine-3-light-2'), $machine3Light3 = $('#machine-3-light-3'), $machine3Light4 = $('#machine-3-light-4'), $machine3Light5 = $('#machine-3-light-5'),
    $machine3Light6 = $('#machine-3-light-6'), $machine3Light7 = $('#machine-3-light-7'),
    $valve = $('#valve'), $saw = $('#saw'), $arm = $('#arm'), $bicep = $('#bicep'), $forearm = $('#forearm'),
    $alarmRed = $('#machine-5-light-bulb-2'), $alarmYellow = $('#machine-5-light-bulb'),
    $howWeHelp = $('#how-we-help'),
    $machinery = $('#machinery'),
    $carding = $('#how-we-help .carding'),
    $content = $('#how-we-help .content');

  var machineTL = new TimelineMax();

  var clearTl = new TimelineMax();

  clearTl

    .set($howWeHelp, {
      yPercent: "+=200",
      autoAlpha: 1
    })
    .set($searchIn, {
      autoAlpha: 0
    })
    .set($designIn, {
      autoAlpha: 0
    })
    .set($inboundIn, {
      autoAlpha: 0
    })
    .set($searchOut, {
      autoAlpha: 0
    })
    .set($designOut, {
      autoAlpha: 0
    })
    .set($inboundOut, {
      autoAlpha: 0
    });

  var clockAndGears = new TimelineMax({
    repeat: -1,
    yoyo: false
  });

  clockAndGears
    .add('conveyer-mobile')
    //.fromTo($clockSecs, 6, {rotation: 0, transformOrigin: 'top center'},{ rotation: 360, ease:Power0.easeNone, immediateRender: false }, 'conveyer-mobile')
    .fromTo($gears, 6, {
      rotation: 0,
      transformOrigin: 'center center'
    }, {
      rotation: 720,
      ease: Power0.easeNone
    }, 'conveyer-mobile')
    .fromTo($conveyerTop, 6, {
      x: '0',
      ease: Power0.easeNone
    }, {
      x: '+=15%',
      ease: Power0.easeNone,
      immediateRender: false
    }, 'conveyer-mobile')
    .fromTo($conveyerBottom, 6, {
      x: '0',
      ease: Power0.easeNone
    }, {
      x: '-=15%',
      ease: Power0.easeNone,
      immediateRender: false
    }, 'conveyer-mobile');

  var searchInMachine = new TimelineMax();

  searchInMachine
    .add('search-stuff-in')
    .to($searchIn, 0.1, {
      autoAlpha: 1,
      scale: 1.2
    }, 'search-stuff-in')
    .to($searchIn, 0.3, {
      scale: 1,
      transformOrigin: 'left top'
    })
    .add('post-it-vacuum', 1)
    .to($postIt1, 0.3, {
      bezier: {
        curviness: 0.3,
        values: path1
      },
      ease: Power4.easeIn
    })
    .to($postIt2, 0.3, {
      bezier: {
        curviness: 0.3,
        values: path2
      },
      ease: Power4.easeIn
    })
    .to($postIt3, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path3
      },
      ease: Power4.easeIn
    }, 'post-it-vacuum+=0.5')
    .to($postIt4, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path4
      },
      ease: Power4.easeIn
    }, 'post-it-vacuum+=0.6')
    .to($postIt5, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path5
      },
      ease: Power4.easeIn
    }, 'post-it-vacuum+=0.7')
    .to($postIt6, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path6
      },
      ease: Power3.easeIn
    }, 'post-it-vacuum+=0.8')
    .to($postIt7, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path2
      },
      ease: Power3.easeIn
    }, 'post-it-vacuum+=0.9')
    .to($postIt8, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path3
      },
      ease: Power3.easeIn
    }, 'post-it-vacuum+=1')
    .to($postIt9, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path4
      },
      ease: Power3.easeIn
    }, 'post-it-vacuum+=1')
    .to($postIt10, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path6
      },
      ease: Power3.easeIn
    }, 'post-it-vacuum+=1')
    .fromTo($glasses, 0.02, {
      rotation: 5,
      transformOrigin: 'center center'
    }, {
      rotation: -5,
      repeat: 10,
      yoyo: true
    }, 'post-it-vacuum+=1')
    .to($glasses, 0.1, {
      bezier: {
        curviness: 0.3,
        values: path0
      },
      ease: Power3.easeIn
    }, 'post-it-vacuum+=1.4')
    .add('post-its-gone');

  var designInMachine = new TimelineMax();

  designInMachine
    .add('design-stuff-in')
    .to($designIn, 0.1, {
      autoAlpha: 1,
      scale: 1.2
    }, 'design-stuff-in')
    .to($designIn, 0.3, {
      scale: 1,
      transformOrigin: 'left top'
    })
    .add('design-vacuum')
    .to($pen1, 0.3, {
      bezier: {
        curviness: 0.3,
        values: path1
      },
      ease: Power4.easeIn
    })
    .to($pen2, 0.3, {
      bezier: {
        curviness: 0.3,
        values: path2
      },
      ease: Power4.easeIn
    })
    .to($pen3, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path2
      },
      ease: Power4.easeIn
    }, 'design-vacuum+=0.5')
    .to($pen4, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path3
      },
      ease: Power4.easeIn
    }, 'design-vacuum+=0.6')
    .to($pen5, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path3
      },
      ease: Power4.easeIn
    }, 'design-vacuum+=0.7')
    .to($pen6, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path4
      },
      ease: Power3.easeIn
    }, 'design-vacuum+=0.8')
    .to($pen7, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path4
      },
      ease: Power3.easeIn
    }, 'design-vacuum+=0.9')
    .to($pen8, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path5
      },
      ease: Power3.easeIn
    }, 'design-vacuum+=1')
    .to($pen9, 0.2, {
      bezier: {
        curviness: 0.3,
        values: path5
      },
      ease: Power3.easeIn
    }, 'design-vacuum+=1')

  var inboundInMachine = new TimelineMax();

  inboundInMachine
    .add('inbound-stuff-in')
    .to($inboundIn, 0.1, {
      autoAlpha: 1,
      scale: 1.2
    }, 'inbound-stuff-in')
    .to($inboundIn, 0.3, {
      scale: 1,
      transformOrigin: 'left top'
    })
    .add('inbound-vacuum')
    .to($material1, 0.3, {
      bezier: {
        curviness: 0.3,
        values: path1
      },
      ease: Power4.easeIn
    })
    .to($material2, 0.3, {
      bezier: {
        curviness: 0.3,
        values: path4
      },
      ease: Power4.easeIn
    })
    .to($material3, 0.5, {
      bezier: {
        curviness: 0.3,
        values: path10
      },
      ease: Power4.easeIn
    }, 'inbound-vacuum+=0.5')
    .to($material4, 0.5, {
      bezier: {
        curviness: 0.3,
        values: path6
      },
      ease: Power4.easeIn
    }, 'inbound-vacuum+=0.6')
    .to($material5, 0.5, {
      bezier: {
        curviness: 0.3,
        values: path10
      },
      ease: Power4.easeIn
    }, 'inbound-vacuum+=0.7')
    .to($material6, 0.5, {
      bezier: {
        curviness: 0.3,
        values: path4
      },
      ease: Power4.easeIn
    }, 'inbound-vacuum+=0.8')

  var movingThroughMachine = new TimelineMax();

  movingThroughMachine
    .set($machine1, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .set($machine2, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .set($machine3, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .set($machine5, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .add('machine-1-action')
    .fromTo($compressor1, 0.6, {
      scaleY: 1,
      transformOrigin: 'bottom center'
    }, {
      scaleY: 0.4,
      ease: Power3.easeInOut,
      repeat: 1,
      yoyo: true
    }, 'machine-1-action-=0.4')
    .fromTo($compressor2, 0.6, {
      scaleY: 1,
      transformOrigin: 'bottom center'
    }, {
      scaleY: 0.4,
      ease: Power3.easeInOut,
      repeat: 1,
      yoyo: true
    }, 'machine-1-action-=0.2')
    .fromTo($machine1, 0.04, {
      rotation: -1,
      transformOrigin: 'center center'
    }, {
      rotation: 2,
      ease: Power0.easeNone,
      repeat: 50,
      yoyo: true
    }, 'machine-1-action')
    .set($machine1, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .to($pushable, 0.2, {
      y: '20'
    }, 'machine-1-action+=0.2')
    .to($lever, 0.2, {
      y: '-20'
    }, 'machine-1-action+=0.4')
    .fromTo($machine2, 0.04, {
      rotation: 0,
      transformOrigin: 'center center'
    }, {
      rotation: -2,
      ease: Power0.easeNone,
      repeat: 50,
      yoyo: true
    }, 'machine-1-action+=0.6')
    .set($machine2, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .to($bar1, 0.1, {
      scaleY: 3,
      transformOrigin: 'bottom center',
      ease: Power4.easeIn
    }, 'machine-1-action+=0.8')
    .to($bar2, 0.1, {
      scaleY: 4,
      transformOrigin: 'bottom center',
      ease: Power4.easeIn
    }, 'machine-1-action+=0.83')
    .to($bar3, 0.1, {
      scaleY: 5,
      transformOrigin: 'bottom center',
      ease: Power4.easeIn
    }, 'machine-1-action+=0.86')
    .to($bar4, 0.1, {
      scaleY: 6,
      transformOrigin: 'bottom center',
      ease: Power4.easeIn
    }, 'machine-1-action+=0.89')
    .to($needle, 0.1, {
      rotation: 30,
      transformOrigin: 'right center'
    }, 'machine-1-action+=1')
    .to($sliderButtons, 0.2, {
      x: '30'
    }, 'machine-1-action+=1')
    .fromTo($machine3, 0.04, {
      rotation: 0,
      transformOrigin: 'center center'
    }, {
      rotation: 3,
      ease: Power0.easeNone,
      repeat: 50,
      yoyo: true
    }, 'machine-1-action+=1.2')
    .set($machine3, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .to($valve, 1, {
      rotation: 1080,
      transformOrigin: 'center center',
      ease: Power3.easeInOut
    }, 'machine-1-action+=1.4')
    .staggerTo($lightSequence, 0.1, {
      fill: '#f9dca7'
    }, 0.1, 'machine-1-action+=1.6')
    .staggerTo($lightSequence, 0.1, {
      fill: '#ff7d62'
    }, 0.1, 'machine-1-action+=1.8')
    .staggerTo($lightSequence, 0.1, {
      fill: '#c45354'
    }, 0.1, 'machine-1-action+=2')
    .staggerTo($lightSequence, 0.1, {
      fill: '#afd0d3'
    }, 0.1, 'machine-1-action+=2.2')
    .staggerTo($lightSequence, 0.1, {
      fill: midTeal
    }, 0.1, 'machine-1-action+=2.4')
    .staggerTo($lightSequence, 0.1, {
      fill: '#3f8faa'
    }, 0.1, 'machine-1-action+=2.6')
    .fromTo($machine5, 0.04, {
      rotation: 0,
      transformOrigin: 'center center'
    }, {
      rotation: 3,
      ease: Power0.easeNone,
      repeat: 50,
      yoyo: true
    }, 'machine-1-action+=2.2')
    .set($machine5, {
      rotation: 0,
      transformOrigin: 'center center'
    })
    .fromTo($alarmRed, 0.3, {
      fill: '#f37c64'
    }, {
      fill: '#f9dca7',
      repeat: 20,
      yoyo: true
    }, 'machine-1-action+=2.4')
    .fromTo($alarmYellow, 0.3, {
      fill: '#f9dca7'
    }, {
      fill: '#f37c64',
      repeat: 20,
      yoyo: true
    }, 'machine-1-action+=2.4')

  ;

  var stuffOutMachine = new TimelineMax();

  stuffOutMachine
    .add('stuff-out')
    .set($searchOut, {
      autoAlpha: 1,
      transformOrigin: 'center center'
    }, 'stuff-out')
    .to($searchOut, 4, {
      xPercent: '+=270',
      ease: Power0.easeNone
    }, 'stuff-out+=0.1')
    .set($designOut, {
      autoAlpha: 1,
      transformOrigin: 'center center'
    }, 'stuff-out+=0.1')
    .to($designOut, 4, {
      xPercent: '+=270',
      ease: Power0.easeNone
    }, 'stuff-out+=1.5')
    .set($inboundOut, {
      autoAlpha: 1,
      transformOrigin: 'center center'
    }, 'stuff-out+=1.5')
    .to($inboundOut, 4.3, {
      xPercent: '+=290',
      ease: Power0.easeNone
    }, 'stuff-out+=3');

machineTL
  .add(clearTl)
  .add(clockAndGears)
  .add(searchInMachine, '0.5')
  .add(designInMachine, '2.5')
  .add(inboundInMachine, '4')
  .add(movingThroughMachine, '5')
  .add(stuffOutMachine, '8');
