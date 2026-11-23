/-
Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Benjamin Stanley Frohman
-/
import TFFrohmanianTether.Basic

/-!
# Vorticity direction: what follows from TF, and what does not

Let \(\tau = \omega/|\omega|\) be the vorticity direction, as written in
`NAMING.md` of `periodic-ns-classical-continuation`
(sha256 `c33b92a54e3ad74bb55f7e003709725cc07dae418ce6d1ab6c73abd742d51fbe`
for the copy in `frohmanian-symplectic-tether-regularity/NAMING.md`).
Let \(\theta(x,y)\) be the angle between \(\omega(x)\) and \(\omega(y)\).
For unit vectors, \(|\sin\theta| = |\tau(x)\times\tau(y)|\).

Beirão da Veiga–Berselli, *Differential and Integral Equations* 15
(2002), 345–356, after Constantin–Fefferman (1993), use a bound of the
form \(|\sin\theta|\le C|x-y|^{1/2}\) (or \(|\sin\theta|\le C|x-y|\))
where \(|\omega|\) is large at both points.

Frohman, *What Is Actually Proved* (9 September 2026, sha256
`0c6b693c00f8e58baa778b642f7a8be41510127125be4e8d187815f1057062ad`),
Definition (def:71), writes
\(|\xi(x,t)-\xi(y,t)|\le C|x-y|^{1/2}\) whenever \(r(x,t),r(y,t)\ge\Omega\).
That paper states that this condition has not been proved for every
smooth divergence-free initial datum. The same project's `NAMING.md`
records parts (A) and (B) of the Frohmanian Tether Hypothesis as open.

This file does not prove Definition (def:71) for every solution. It
records algebraic facts needed to test the claim:

* \(|\sin\theta|\) and \(|\tau(x)-\tau(y)|\) are not interchangeable:
  if \(\theta=\pi\), then \(\sin\theta=0\) while \(|\tau(x)-\tau(y)|=2\).
* In the projected-kernel reading of TF, with \(\delta H=u\), the
  tether contribution along the kinetic-energy Hamiltonian vanishes
  (`Pi_u_tether_contribution_along_H`), so TF does not add a term to
  the Navier–Stokes vorticity equation from which a direction bound
  could be derived.
-/

namespace TFFrohmanianTether

/-- \(|\sin\theta|^2 = |\tau\times\eta|^2\) for \(\tau,\eta\in\mathbb{R}^3\). -/
def sin_theta_sq (τ η : Fin 3 → ℝ) : ℝ := dot (cross τ η) (cross τ η)

theorem sin_theta_sq_of_parallel (τ : Fin 3 → ℝ) : sin_theta_sq τ τ = 0 := by
  have hc : cross τ τ = fun _ => 0 := by
    funext i
    fin_cases i <;> simp [cross] <;> ring
  simp [sin_theta_sq, hc, dot]

/-- If \(\eta = -\tau\), then \(\theta=\pi\), so \(\sin\theta=0\). -/
theorem sin_theta_sq_of_antiparallel (τ : Fin 3 → ℝ) :
    sin_theta_sq τ (fun i => -τ i) = 0 := by
  have hc : cross τ (fun i => -τ i) = fun _ => 0 := by
    funext i
    fin_cases i <;> simp [cross] <;> ring
  simp [sin_theta_sq, hc, dot]

/-- If \(\eta = -\tau\) and \(\tau = e_1\), then \(|\tau-\eta|=2\), while \(\sin\theta=0\).
Thus \(|\sin\theta|\) and \(|\tau-\eta|\) are not the same quantity. -/
theorem antiparallel_direction_gap :
    sin_theta_sq e₁ (fun i => -e₁ i) = 0 ∧
      dot (fun i => e₁ i - (-e₁ i)) (fun i => e₁ i - (-e₁ i)) = 4 := by
  constructor
  · exact sin_theta_sq_of_antiparallel e₁
  · simp [dot, e₁]
    norm_num

/-- Re-stated from `Basic.lean`: the projected TF contribution along \(H\),
with \(\delta H=u\), is zero. No direction bound is obtained from this term. -/
theorem projected_TF_adds_nothing_along_H (κ : ℝ) (ω u δF : Fin 3 → ℝ) :
    -κ * omega_sq_dot ω (Pi_u u δF) (Pi_u u u) = 0 :=
  Pi_u_tether_contribution_along_H κ ω u δF

end TFFrohmanianTether
