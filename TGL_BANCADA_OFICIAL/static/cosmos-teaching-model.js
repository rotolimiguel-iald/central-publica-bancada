/* Isolated teaching reference. No scientific engine or data dependency. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else {
    root.CosmosTeaching = factory();
  }
})(typeof window !== 'undefined' ? window : globalThis, function () {
  'use strict';

  const MAX_Z = 100000;
  const HISTORY_INTERVALS = 240;
  const PARAMETER_KEYS = ['omegaB', 'omegaC', 'omegaR'];
  const formula = 'E²(z) = Ω_b(1+z)³ + Ω_c(1+z)³ + Ω_r(1+z)⁴ + Ω_Λ';
  const metadata = Object.freeze({
    id: 'FLAT_FLRW_TEACHING_V1',
    status: 'DIDACTIC_REFERENCE_NOT_TGL_PREDICTION',
    parameterProvenance: 'User-specified rounded teaching parameters; not a Planck posterior.',
    formula,
    omegaLambdaFormula: 'Ω_Λ = 1 − Ω_b − Ω_c − Ω_r',
    scaleFactorFormula: 'a = 1/(1+z)',
    fractionFormula: 'f_i(z) = densities[i]/E²(z)',
    densityNormalization: 'rho_i(z)/rho_crit(0); dimensionless, not an absolute physical density',
    expansionNormalization: 'E(z) = H(z)/H0',
    domain: Object.freeze({minRedshift: 0, maxRedshift: MAX_Z}),
    assumptions: Object.freeze([
      'Spatially flat FLRW background.',
      'Nonrelativistic baryons and dark matter scale as a^-3.',
      'Idealized radiation scales as a^-4.',
      'Dark energy is a cosmological constant with w=-1.',
    ]),
    limitations: Object.freeze([
      'No TGL prediction, beta parameter, or inference from observations.',
      'No CAMB, spectra, physical age, or calculated structure formation.',
      'Fixed idealized component scaling; no detailed thermal or species evolution.',
    ]),
    historySampling: Object.freeze({
      coordinate: 'log(1+z)', count: HISTORY_INTERVALS + 1,
      endpointsIncluded: true,
    }),
  });

  function defaultParameters() {
    return {omegaB: 0.049, omegaC: 0.266, omegaR: 0.000092};
  }

  function validateParameters(p) {
    if (p === null || typeof p !== 'object' || Array.isArray(p) ||
        Object.keys(p).length !== PARAMETER_KEYS.length ||
        !PARAMETER_KEYS.every(key => Object.prototype.hasOwnProperty.call(p, key))) {
      throw new TypeError('Expected exactly omegaB, omegaC and omegaR.');
    }
    const parameters = {};
    for (const key of PARAMETER_KEYS) {
      const value = p[key];
      if (!Number.isFinite(value)) throw new TypeError(key + ' must be a finite number.');
      if (value < 0) throw new RangeError(key + ' must be nonnegative.');
      parameters[key] = value;
    }
    const total = parameters.omegaB + parameters.omegaC + parameters.omegaR;
    if (!(total < 1)) throw new RangeError('omegaB + omegaC + omegaR must be less than 1.');
    parameters.omegaLambda = 1 - total;
    return parameters;
  }

  function calculate(z, p) {
    const onePlusZ = 1 + z;
    const matterScale = onePlusZ ** 3;
    const densities = {
      baryons: p.omegaB * matterScale,
      darkMatter: p.omegaC * matterScale,
      radiation: p.omegaR * onePlusZ ** 4,
      darkEnergy: p.omegaLambda,
    };
    const E2 = densities.baryons + densities.darkMatter + densities.radiation + densities.darkEnergy;
    const fractions = {};
    for (const key of Object.keys(densities)) fractions[key] = densities[key] / E2;
    return {z, a: 1 / onePlusZ, E: Math.sqrt(E2), omegaLambda: p.omegaLambda, fractions, densities};
  }

  function evaluate(z, p) {
    if (!Number.isFinite(z)) throw new TypeError('z must be a finite number.');
    if (z < 0 || z > MAX_Z) throw new RangeError('z must be within [0, 100000].');
    return calculate(z, validateParameters(p));
  }

  function history(p) {
    const parameters = validateParameters(p);
    const upper = Math.log1p(MAX_Z);
    return Array.from({length: HISTORY_INTERVALS + 1}, (_, i) => {
      const z = i === 0 ? 0 : i === HISTORY_INTERVALS ? MAX_Z : Math.expm1(upper * i / HISTORY_INTERVALS);
      return calculate(z, parameters);
    });
  }

  return Object.freeze({defaultParameters, evaluate, history, formula, metadata});
});
