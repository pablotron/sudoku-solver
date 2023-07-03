(() => {
  'use strict';
  const D = document;
  const get = (id) => D.getElementById(id);
  const on = (id, ev, fn) => get(id).addEventListener(ev, fn);

  const SAMPLE = [
    8, 0, 0,  0, 0, 0,  0, 0, 0,
    0, 0, 3,  6, 0, 0,  0, 0, 0,
    0, 7, 0,  0, 9, 0,  2, 0, 0,

    0, 5, 0,  0, 0, 7,  0, 0, 0,
    0, 0, 0,  0, 4, 5,  7, 0, 0,
    0, 0, 0,  1, 0, 0,  0, 3, 0,

    0, 0, 1,  0, 0, 0,  0, 6, 8,
    0, 0, 8,  5, 0, 0,  0, 1, 0,
    0, 9, 0,  0, 0, 0,  4, 0, 0,
  ];

  // get grid as string
  const get_grid_string = () => {
    let r = new Array(81);
    for (let i = 0; i < 81; i++) {
      const val = get(`c${i}`).value;
      r[i] = val.match(/^[1-9]$/) ? val : '0';
    }
    return r.join('');
  };

  // solve grid
  const solve = () => {
    // send request
    fetch('./solve', {
      method: 'POST',

      headers: {
        'content-type': 'application/json',
      },

      body: JSON.stringify({
        grid: get_grid_string(),
      }),
    }).then((r) => r.json()).then((r) => {
      // check for solution
      if (!r.solution || !r.solution.length) {
        alert('no solution');
        return;
      }

      // check solution
      if (r.solution.length !== 81 || !r.solution.match(/^[0-9]{81}$/)) {
        console.log({ err: 'invalid solution', r: r});
        alert('got invalid solution from server');
        return;
      }

      // show solution
      r.solution.split('').forEach((d, i) => { get(`c${i}`).value = d });
    });
  };

  // reset to sample grid
  const reset = () => {
    for (let i = 0; i < 81; i++) {
      get(`c${i}`).value = SAMPLE[i] || '';
    }
  };

  const confirm_reset = () => {
    if (confirm('Reset grid?')) {
      reset();
    }
  };

  // clear grid
  const confirm_clear = () => {
    if (confirm('Clear grid?')) {
      for (let i = 0; i < 81; i++) {
        get(`c${i}`).value = '';
      }
    }
  };

  D.addEventListener('DOMContentLoaded', () => {
    reset();
    on('solve', 'click', solve);
    on('reset', 'click', confirm_reset);
    on('clear', 'click', confirm_clear);
  });
})();
