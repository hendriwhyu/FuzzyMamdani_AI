import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definisikan variabel input
usia_ibu = ctrl.Antecedent(np.arange(0, 51, 1), 'usia_ibu')
lila = ctrl.Antecedent(np.arange(0, 40, 0.1), 'lila')
lingkar_perut = ctrl.Antecedent(np.arange(60, 121, 1), 'lingkar_perut')
imt = ctrl.Antecedent(np.arange(15, 36, 0.1), 'imt')
jarak_kehamilan = ctrl.Antecedent(np.arange(0, 5, 0.1), 'jarak_kehamilan')
jumlah_anak = ctrl.Antecedent(np.arange(0, 11, 1), 'jumlah_anak')
anemia = ctrl.Antecedent(np.arange(0, 2, 1), 'anemia')

# Definisikan variabel output
stunting = ctrl.Consequent(np.arange(0, 101, 1), 'stunting')

# Fuzzifikasi untuk variabel input
usia_ibu['young'] = fuzz.trimf(usia_ibu.universe, [0, 0, 19])
usia_ibu['middle'] = fuzz.trimf(usia_ibu.universe, [19, 27, 35])
usia_ibu['old'] = fuzz.trimf(usia_ibu.universe, [35, 50, 50])

lila['small'] = fuzz.trimf(lila.universe, [0, 0, 23.5])
lila['medium'] = fuzz.trimf(lila.universe, [23.5, 25, 26.5])
lila['large'] = fuzz.trimf(lila.universe, [26.5, 40, 40])

lingkar_perut['normal'] = fuzz.trimf(lingkar_perut.universe, [60, 80, 80])
lingkar_perut['big'] = fuzz.trimf(lingkar_perut.universe, [80, 100, 120])

imt['underweight'] = fuzz.trimf(imt.universe, [15, 15, 18.5])
imt['normal'] = fuzz.trimf(imt.universe, [18.5, 22, 25])
imt['overweight'] = fuzz.trimf(imt.universe, [25, 30, 35])

jumlah_anak['small'] = fuzz.trimf(jumlah_anak.universe, [0, 0, 3])
jumlah_anak['medium'] = fuzz.trimf(jumlah_anak.universe, [3, 5, 7])
jumlah_anak['big'] = fuzz.trimf(jumlah_anak.universe, [7, 10, 10])

anemia['no'] = fuzz.trimf(anemia.universe, [0, 0, 0])
anemia['yes'] = fuzz.trimf(anemia.universe, [1, 1, 1])

# Fuzzifikasi untuk variabel output
stunting['low'] = fuzz.trimf(stunting.universe, [0, 0, 25])
stunting['medium'] = fuzz.trimf(stunting.universe, [25, 50, 75])
stunting['high'] = fuzz.trimf(stunting.universe, [75, 100, 100])
stunting['very_low'] = fuzz.trimf(stunting.universe, [0, 0, 10])
stunting['very_high'] = fuzz.trimf(stunting.universe, [90, 100, 100])

# Definisikan aturan-aturan fuzzy
rule1 = ctrl.Rule(usia_ibu['young'] | usia_ibu['old'] &
                  lila['small'] & lingkar_perut['big'] &
                  imt['underweight'] | imt['overweight'] & jumlah_anak['big'] &
                  anemia['yes'], stunting['high'])

# Definisikan aturan fuzzy untuk stunting low
rule2 = ctrl.Rule(usia_ibu['middle'] &
                  lila['medium'] | lila['large'] &
                  lingkar_perut['normal'] &
                  imt['normal'] | imt['overweight'] &
                  jumlah_anak['small'] &
                  anemia['no'], stunting['low'])
# Definisikan aturan fuzzy untuk stunting high
rule3 = ctrl.Rule(usia_ibu['middle'] | usia_ibu['old'] &
                  lila['small'] | lila['medium'] &
                  lingkar_perut['big'] &
                  imt['underweight'] | imt['overweight'] &
                  jumlah_anak['medium'] | jumlah_anak['big'] &
                  anemia['yes'], stunting['high'])

# Definisikan aturan fuzzy untuk stunting medium
rule4 = ctrl.Rule(usia_ibu['middle'] | usia_ibu['old'] &
                  lila['medium'] | lila['large'] &
                  lingkar_perut['big'] &
                  imt['normal'] | imt['overweight'] &
                  jumlah_anak['medium'] | jumlah_anak['big'] &
                  anemia['no'], stunting['medium'])

# Definisikan aturan fuzzy untuk stunting very low
rule5 = ctrl.Rule(usia_ibu['young'] &
                  lila['small'] &
                  lingkar_perut['normal'] &
                  imt['underweight'] &
                  jumlah_anak['small'] &
                  anemia['no'], stunting['very_low'])

# Definisikan aturan fuzzy untuk stunting very high
rule6 = ctrl.Rule(usia_ibu['young'] | usia_ibu['old'] &
                  lila['small'] &
                  lingkar_perut['big'] &
                  imt['underweight'] | imt['overweight'] &
                  jumlah_anak['medium'] | jumlah_anak['big'] &
                  anemia['yes'], stunting['very_high'])

# Definisikan sistem kontrol
stunting_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
stunting_sim = ctrl.ControlSystemSimulation(stunting_ctrl)

# Menerima input dari pengguna
usia_ibu_input = float(input("Masukkan usia ibu (0-50): "))
lila_input = float(input("Masukkan lingkar lengan atas (Lila) (0-39.9): "))
lingkar_perut_input = float(input("Masukkan lingkar perut (60-120): "))
imt_input = float(input("Masukkan Indeks Massa Tubuh (IMT) (15-35): "))
jumlah_anak_input = int(input("Masukkan jumlah anak (0-10): "))
anemia_input = int(input("Apakah ibu menderita anemia? (0: tidak, 1: ya): "))

# Masukkan nilai input ke dalam simulasi
stunting_sim.input['usia_ibu'] = usia_ibu_input
stunting_sim.input['lila'] = lila_input
stunting_sim.input['lingkar_perut'] = lingkar_perut_input
stunting_sim.input['imt'] = imt_input
stunting_sim.input['jumlah_anak'] = jumlah_anak_input
stunting_sim.input['anemia'] = anemia_input

try:
    stunting_sim.compute()
    result = stunting_sim.output['stunting']

    print("Hasil defuzzifikasi:", result)

    max_activation = -np.inf
    selected_stunting = None

    for label, membership in stunting.terms.items():
        activation = fuzz.interp_membership(
            stunting.universe, membership.mf, result)
        if activation > max_activation:
            max_activation = activation
            selected_stunting = label

    if selected_stunting is not None:
        print("Status stunting:", selected_stunting)
    else:
        print("Status stunting: Unknown")

except ValueError:
    print("Rule tidak didefinisikan.")
