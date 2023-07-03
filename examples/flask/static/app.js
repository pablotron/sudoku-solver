(() => {
  'use strict';
  const D = document;
  const get = (id) => D.getElementById(id);
  const on = (id, ev, fn) => get(id).addEventListener(ev, fn);

  // get grid as string
  const to_string = () => {
    let r = new Array(81);
    for (let i = 0; i < 81; i++) {
      const val = get(`c${i}`).value;
      r[i] = val.match(/^[1-9]$/) ? val : '0';
    }
    return r.join('');
  };

  const set_grid = (s) => {
    // check grid
    if (s.length !== 81 || !s.match(/^[0-9]{81}$/)) {
      alert('invalid grid');
      return;
    }

    // show grid
    s.split('').forEach((d, i) => { get(`c${i}`).value = +d || '' });
  };

  // solve grid
  const solve = () => {
    // send request
    fetch('./solve', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ grid: to_string() }),
    }).then((r) => r.json()).then((r) => {
      // check for solution
      if (!r.grid || !r.grid.length) {
        alert('no solution');
        return;
      }

      // show solution
      set_grid(r.grid);
    });
  };

  // reset to default grid
  const reset = () => {
    set_grid(get('reset').dataset.grid);
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
