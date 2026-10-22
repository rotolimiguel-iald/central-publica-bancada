"""Independent original/transformed-phase quadratures with full-wave controls."""
import json
import time
import numpy as np
from scipy.special import logsumexp
import source_evidence as se
import peak_phase_coordinates as pc


def main():
    state = se.load_state()
    rows = []
    failures = []
    # Includes the unequal-mass source where odd harmonics carry information.
    for family in se.FAMILIES:
        for source in (se.SOURCES[0], se.SOURCES[2]):
            x = se.source_vector(source)
            t0 = time.monotonic()
            bank = pc.phase_bank(family, x, state["times"], state["O5_white"])
            targets = state["O5_targets"][[0, 6, 500, 506]]
            controls = []
            for phase in (.173, .619, 1.413, 2.231, 4.877):
                y = x.copy()
                y[5] = phase
                pair, meta = se.paired_polarizations(family, y, state["times"])
                for a in (0, 1):
                    expected = se.basis_from_polarizations(pair[a], state["O5_white"])
                    got = pc.evaluate_bank(bank, [phase], a)[0]
                    relative = float(np.linalg.norm(got-expected)/np.linalg.norm(expected))
                    _, direct_ll = se.linear_statistics(expected, targets, 3.)
                    fourier_ll = pc.bank_loglikes(bank, [phase], targets, a)
                    error = float(np.max(np.abs(direct_ll-fourier_ll)))
                    controls.append(dict(phase=phase, a=a, waveform_relative_error=relative, logL_error=error))
                    if relative > 1e-6 or error > .001:
                        failures.append(dict(family=family, source=source["name"], phase=phase, a=a, reason="phase_interpolation", error=error))
            checks = []
            for a in (0, 1):
                regular = pc.phase_integral(bank, targets, a, 512)
                transformed = pc.phase_integral(bank, targets, a, 512, transformed=True)
                refined = pc.phase_integral(bank, targets, a, 1024)
                quadrature = float(np.max(np.abs(refined-regular)))
                equivalence = float(np.max(np.abs(transformed-refined)))
                # Adversarial single-branch omission: don't assume 22 exhausts
                # the full wave; expose its numerical difference if present.
                zeta = np.pi*np.arange(512)/512
                first = pc.bank_loglikes(bank, zeta+bank["phase_reference"]/2, targets, a)
                single_branch = logsumexp(first, axis=0)-np.log(512)
                odd_difference = float(np.max(np.abs(single_branch-refined)))
                checks.append(dict(a=a, quadrature_512_1024=quadrature, coordinate_change_error=equivalence,
                                   error_if_only_one_branch_kept=odd_difference))
                if quadrature > 1e-5 or equivalence > 1e-5:
                    failures.append(dict(family=family, source=source["name"], a=a, reason="phase_quadrature", error=max(quadrature, equivalence)))
            # The phi=0 / phi=pi complete signals retain any odd-m contribution.
            branch_norm = float(np.linalg.norm(pc.evaluate_bank(bank, [0.], 0)[0]-pc.evaluate_bank(bank, [np.pi], 0)[0]))
            row = dict(family=family, source=source["name"], direct_controls=controls, quadratures=checks,
                       full_signal_branch_difference_norm=branch_norm, seconds=time.monotonic()-t0)
            rows.append(row)
            print(json.dumps(dict(family=family, source=source["name"], max_waveform_error=max(c["waveform_relative_error"] for c in controls),
                                  max_logL_error=max(c["logL_error"] for c in controls), quadratures=checks)), flush=True)
    result = dict(status="PASS_PRIOR_PRESERVING_PHASE_COORDINATES" if not failures else "FAIL_PHASE_CONTROL", rows=rows, failures=failures,
                  physical_prior_unchanged=True, both_phase_branches_included=True, source_dimensions_integrated=0,
                  no_C6_change=se.sha(se.ROOT/"REGISTRO_C6.json")==se.sha(se.ROOT.parent.parent/"REGISTRO_C6.json"),
                  scope="Coordinate map and conditional phase quadrature tested, not an accepted source evidence or universal error bound",
                  hashes={n:se.sha(se.ROOT/n) for n in ("peak_phase_coordinates.py", "validate_peak_phase_coordinates.py", "REGISTRATION.json", "INJECTIONS.json")})
    se.write(se.ROOT/"PEAK_PHASE_COORDINATES_VALIDATION.json", result)
    if failures:
        raise ValueError("Phase control failed; preserve result and inspect")


if __name__ == "__main__":
    main()
