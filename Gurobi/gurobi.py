from gurobipy import GRB, Model, quicksum
from random import seed

import parametros as p

seed(10)  # Seed para reproducibilidad


class GurobiModel():
    """"
    Descripción: Esta clase contiene el modelo de optimización.
    """

    def __init__(self):
        # Descripción: Esta función inicializa el modelo.
        self.model = Model()
        self.asignar_sets()
        self.asignar_variables()
        self.asignar_restricciones()
        self.finalizar_modelo()

    def asignar_sets(self):
        # Descripción: Esta función asigna los sets del modelo.
        global I, J, K, L
        I = p.I
        J = p.J
        K = p.K
        L = p.L

    def asignar_variables(self):
        # Descripción: Esta función asigna las variables del modelo.
        global beta, w, x, q, z, y, alpha
        beta = self.model.addVars(I, vtype=GRB.BINARY, name="b_i")
        w = self.model.addVars(I, J, L, vtype=GRB.INTEGER, name="w_ijl")
        x = self.model.addVars(I, J, L, vtype=GRB.INTEGER, name="x_ijl")
        q = self.model.addVars(K, J, vtype=GRB.INTEGER, name="q_kj")
        z = self.model.addVars(K, J, vtype=GRB.INTEGER, name="z_kj")
        y = self.model.addVars(J, L, vtype=GRB.INTEGER, name="y_jl")
        alpha = self.model.addVars(J, vtype=GRB.CONTINUOUS, name="alpha_j")

    def asignar_restricciones(self):
        # Descripción: Esta función asigna las restricciones del modelo.

        # Restricción 1: Total de presupuesto no puede ser menor a la suma de presupuestos mensuales
        self.model.addConstr(
            (quicksum(alpha[j] for j in J) <= p.PT), name="R1")

        # Restricción 2: Paneles no pueden superar el espacio total de cada suelo.
        self.model.addConstrs((quicksum(w[i, j, l] * (p.T[i]) for i in I for j in J)
                               <= p.EA[l] for l in L), name="R2")

        # Restricción 3: Todos los paneles (no del techo) deben ser cuidados.
        self.model.addConstrs(
            (quicksum(w[i, j, 1] for i in I) <= p.PC * y[j, 1] for j in J), name="R3_1")
        self.model.addConstr((quicksum(y[j, 2] for j in J) == 0), name="R3_2")

        # Restricción 4: Relación entre los paneles operativos y los instalados.
        self.model.addConstrs((w[i, j - 1, l] + x[i, j, l] == w[i, j, l]
                              for i in I for j in J for l in L if j != 1), name="R4_1")

        self.model.addConstrs((x[i, 1, l] == w[i, 1, l]
                              for i in I for l in L), name="R4_2")

        # Restricción 5: Solamente se puede implementar paneles de un tipo.
        self.model.addConstr((quicksum(beta[i] for i in I) <= 1), name="R5")

        # Restricción 6: No se pueden operar paneles de un tipo distinto al implementado.
        self.model.addConstrs(
            (quicksum(x[i, j, l] for l in L for j in J) <= p.M * beta[i] for i in I), name="R6")

        # Restricción 7: Relación entre inversores operativos y los instalados
        # (No hay operativos al comienzo)
        self.model.addConstrs((q[k, j - 1] + z[k, j] == q[k, j]
                              for k in K for j in J if j != 1), name="R7_1")

        self.model.addConstrs((z[k, 1] == q[k, 1]
                              for k in K), name="R7_2")

        # self.model.addConstrs((q[k, 0] == 0 for k in K), name="R7_2")

        # Restricción 8: Se respeta la capacidad de cada inversor.
        self.model.addConstrs((quicksum(w[i, j, l] for i in I) <= quicksum(p.muZ[i, k]
                               * q[k, j] for i in I) for k in K for l in L for j in J), name="R8")

        # Restricción 9: El presupuesto mensual no puede ser menor a los gastos incurridos en el mes
        self.model.addConstrs(((quicksum(((p.C[i] + p.CT[i] + p.CI[i]) * x[i, j, l] + p.CM[i] *
                                          w[i, j, l]) for i in I for l in L) +
                                (quicksum(p.SC * y[j, l] for l in L)) +
                                (quicksum((p.CZ[k] + p.CTZ[k] + p.CIZ[k]) * z[k, j] + p.CMZ[k]
                                          * q[k, j] for k in K))) <= alpha[j] for j in J),
                              name='R9')

    def finalizar_modelo(self):
        # Descripción: Esta función asigna la función objetivo del modelo y lo finaliza.
        fo = (quicksum(w[i, j, l] * p.E[i, j]
              for i in I for j in J for l in L))

        self.model.update()
        self.model.setObjective(fo, GRB.MAXIMIZE)
        self.model.setParam("TimeLimit", 1800)  # 30 Minutos TimeLimit
        self.model.optimize()

        self.model.printAttr('X')
