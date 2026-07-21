/* =============================================================================
   construct.js — a minimal constraint-geometry kernel, in GeoGebra's paradigm.

   WHY THIS EXISTS
   ---------------
   A .ggb file is a ZIP whose payload is geogebra.xml — and that XML is not a
   drawing program. It is a DECLARED CONSTRUCTION:

       <element type="point" label="A"/>                          free object
       <command name="Circle"><input a0="A" a1="B"/>
                              <output a0="c"/></command>          dependent object
       <command name="Intersect"><input a0="c" a1="d" a2="2"/>
                                 <output a0="C"/></command>       dependent object

   Free objects are the roots; dependent objects are functions of previously
   declared objects; the kernel evaluates the graph in order and re-solves on any
   change. That is why dragging a point in GeoGebra keeps every derived object
   exact: correctness is a consequence of the CONSTRUCTION, not of the author's
   arithmetic in a draw loop.

   This module is that idea in ~90 lines, with no dependencies, so the site's
   instruments can be declared rather than plotted — and still ship self-contained.

   USAGE
   -----
       var C = new Construct.Construction();
       C.free('O','point',{x:0,y:0});
       C.free('r','number',1);
       C.dep('c','circle',['O','r'], (O,r) => ({cx:O.x, cy:O.y, r:r}));
       C.free('P','point',{x:0.45,y:0.28});
       C.dep('Pp','point',['P','c'], Construct.G.inversion);   // P' = Inversion(P,c)
       C.dep('k','number',['O','P','Pp'], (O,P,Pp) =>
             Construct.G.dist(O,P) * Construct.G.dist(O,Pp));  // ≡ r², by construction
       C.solve();
       C.set('P', {x:0.9, y:0.1});      // move a free object; everything downstream follows

   DISCIPLINE
   ----------
   - Declare in dependency order (a dependent object may only cite objects already
     declared). This makes declaration order a valid topological order, exactly as
     GeoGebra's construction list does.
   - Dependent functions must be PURE: value in, value out, no drawing, no state.
   - Rendering reads C.val(label); it never writes. Model and view stay separate.
   ============================================================================= */
(function (global) {
  'use strict';

  function Construction() {
    this.objects = Object.create(null);
    this.order = [];
    this.onSolve = null;
  }

  /* Declare a root object: a point {x,y}, a number, or anything a dependent reads. */
  Construction.prototype.free = function (label, type, value) {
    if (this.objects[label]) throw new Error('construct: duplicate label "' + label + '"');
    this.objects[label] = { label: label, type: type, free: true, value: value, ins: [] };
    this.order.push(label);
    return this;
  };

  /* Declare a dependent object: its value is fn(...values of ins). */
  Construction.prototype.dep = function (label, type, ins, fn) {
    if (this.objects[label]) throw new Error('construct: duplicate label "' + label + '"');
    for (var i = 0; i < ins.length; i++) {
      if (!this.objects[ins[i]]) {
        throw new Error('construct: "' + label + '" cites undeclared "' + ins[i] +
                        '" — declare inputs first (dependency order).');
      }
    }
    this.objects[label] = { label: label, type: type, free: false, ins: ins, fn: fn, value: undefined };
    this.order.push(label);
    return this;
  };

  /* Evaluate the whole graph in declaration order. */
  Construction.prototype.solve = function () {
    for (var i = 0; i < this.order.length; i++) {
      var o = this.objects[this.order[i]];
      if (o.free) continue;
      var args = new Array(o.ins.length);
      for (var j = 0; j < o.ins.length; j++) args[j] = this.objects[o.ins[j]].value;
      o.value = o.fn.apply(null, args);
    }
    if (this.onSolve) this.onSolve(this);
    return this;
  };

  Construction.prototype.val = function (label) {
    var o = this.objects[label];
    if (!o) throw new Error('construct: no object "' + label + '"');
    return o.value;
  };

  /* Move a free object and re-solve. Dependents are read-only by design. */
  Construction.prototype.set = function (label, value) {
    var o = this.objects[label];
    if (!o) throw new Error('construct: no object "' + label + '"');
    if (!o.free) throw new Error('construct: "' + label + '" is dependent — move its inputs instead.');
    o.value = value;
    return this.solve();
  };

  Construction.prototype.isFree = function (label) { return !!this.objects[label].free; };

  /* Human-readable construction listing — the model, printable (like geogebra.xml). */
  Construction.prototype.listing = function () {
    var self = this;
    return this.order.map(function (l) {
      var o = self.objects[l];
      return o.free ? (l + ' = free ' + o.type)
                    : (l + ' = ' + o.type + '(' + o.ins.join(', ') + ')');
    });
  };

  /* ---- geometric primitives (pure) ---------------------------------------- */
  var G = {
    dist: function (A, B) { return Math.hypot(B.x - A.x, B.y - A.y); },

    /* Circle inversion — the native primitive. On the positive real axis with the
       unit circle this IS x ↦ 1/x. Invariant: |OP|·|OP'| = r². */
    inversion: function (P, c) {
      var dx = P.x - c.cx, dy = P.y - c.cy, d2 = dx * dx + dy * dy;
      if (d2 < 1e-12) return { x: Infinity, y: Infinity };
      var k = (c.r * c.r) / d2;
      return { x: c.cx + dx * k, y: c.cy + dy * k };
    },

    /* Point reflection through O — the half-twist u ↦ −u. */
    pointReflect: function (P, O) { return { x: 2 * O.x - P.x, y: 2 * O.y - P.y }; },

    circle: function (O, r) { return { cx: O.x, cy: O.y, r: r }; },

    /* Suda's egg / Cayley coordinate and its inverse (real branch). */
    cayley: function (x) { return (x - 1) / (x + 1); },
    cayleyInv: function (u) { return (1 + u) / (1 - u); },

    /* Stereographic projection from the north pole onto the equatorial plane,
       and its inverse — the D2 chart. */
    toSphere: function (X, Y) {
      var d = X * X + Y * Y + 1;
      return { x: 2 * X / d, y: 2 * Y / d, z: (X * X + Y * Y - 1) / d };
    },

    midpoint: function (A, B) { return { x: (A.x + B.x) / 2, y: (A.y + B.y) / 2 }; }
  };

  global.Construct = { Construction: Construction, G: G };
})(typeof window !== 'undefined' ? window : this);
