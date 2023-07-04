(() => {
  'use strict';
  const D = document;
  const get = (id) => D.getElementById(id);
  const on = (id, ev, fn) => get(id).addEventListener(ev, fn);
  const ask = (m, f) => (() => confirm(m) && f());

  // get grid as string
  const to_string = () => {
    let r = new Array(81);
    for (let i = 0; i < 81; i++) {
      const val = get(`c${i}`).value;
      r[i] = val.match(/^[1-9]$/) ? val : '0';
    }
    return r.join('');
  };

  // set grid from string
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
    fetch('solve', {
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

  // download grid as text file
  const download = () => {
    const q = new URLSearchParams({ grid: to_string() });
    location.href = `download?${q}`;
  };

  // reset grid
  const reset = () => set_grid(get('grid').dataset.reset);

  // clear grid
  const clear = () => D.querySelectorAll('#grid input').forEach(e => e.value = '');

  D.addEventListener('DOMContentLoaded', () => {
    // reset grid
    reset();

    // bind to events
    on('solve', 'click', solve);
    on('download', 'click', download);
    on('reset', 'click', ask('Reset grid?', reset));
    on('clear', 'click', ask('Clear grid?', clear));
  });
})();
