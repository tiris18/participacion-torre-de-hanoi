import time
import tkinter as tk
from tkinter import messagebox

# ==========================================
# 1. IMPLEMENTACIÓN DE LA CLASE STACK (PILA)
# ==========================================
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def size(self):
        return len(self.items)

    def get_elements(self):
        return self.items


# ==========================================
# 2. IMPLEMENTACIÓN DE LA APLICACIÓN GRÁFICA
# ==========================================
class TorreHanoiPilaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torre de Hanói - Clase Stack con Cálculo de Tiempo Real")
        self.root.geometry("750x580")
        self.root.config(bg="#f8f9fa")
        self.root.resizable(False, False)

        self.num_discos = 5
        
        self.torres = {
            "Origen": Stack(),
            "Auxiliar": Stack(),
            "Destino": Stack()
        }
        
        self.movimientos_totales = 0
        self.en_proceso = False

        # --- INTERFAZ GRÁFICA ---
        titulo = tk.Label(root, text="Torre de Hanói (Estructura Stack + Análisis Temporal)", font=("Arial", 15, "bold"), bg="#f8f9fa", fg="#2c3e50")
        titulo.pack(pady=10)

        # Panel de Controles
        frame_controles = tk.Frame(root, bg="#f8f9fa")
        frame_controles.pack(pady=5)

        tk.Label(frame_controles, text="Número de Discos:", font=("Arial", 11), bg="#f8f9fa").grid(row=0, column=0, padx=5)
        self.entry_discos = tk.Entry(frame_controles, font=("Arial", 11), width=6, justify="center")
        self.entry_discos.insert(0, "5")
        self.entry_discos.grid(row=0, column=1, padx=5)

        self.btn_iniciar = tk.Button(frame_controles, text="Iniciar Resolución", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=self.iniciar_animacion)
        self.btn_iniciar.grid(row=0, column=2, padx=10)

        self.btn_rendimiento = tk.Button(frame_controles, text="Medir Tiempos (5, 10, 30, 64)", bg="#2980b9", fg="white", font=("Arial", 10, "bold"), command=self.medir_tiempos_consola)
        self.btn_rendimiento.grid(row=0, column=3, padx=10)

        # Canvas para dibujar las torres y los discos
        self.canvas = tk.Canvas(root, width=700, height=300, bg="white", highlightthickness=2, highlightbackground="#bdc3c7")
        self.canvas.pack(pady=10)

        # Etiqueta de contador de movimientos
        self.lbl_contador = tk.Label(root, text="Movimientos: 0", font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#e67e22")
        self.lbl_contador.pack(pady=2)

        # Etiqueta de desglose de tiempo para 64 discos
        self.lbl_tiempo_real = tk.Label(root, text="", font=("Arial", 10, "bold"), bg="#f8f9fa", fg="#c0392b", justify="center")
        self.lbl_tiempo_real.pack(pady=5)

        self.reiniciar_estructuras()
        self.dibujar_torres()

    def reiniciar_estructuras(self):
        try:
            val = int(self.entry_discos.get())
            if val < 1:
                messagebox.showwarning("Aviso", "Ingresa al menos 1 disco.")
                return False
            self.num_discos = val
        except ValueError:
            messagebox.showerror("Error", "Ingresa un número válido de discos.")
            return False

        self.torres["Origen"] = Stack()
        self.torres["Auxiliar"] = Stack()
        self.torres["Destino"] = Stack()

        for i in range(self.num_discos, 0, -1):
            self.torres["Origen"].push(i)

        self.movimientos_totales = 0
        
        # Si configuran 64 discos, calculamos inmediatamente el tiempo real en la interfaz
        if self.num_discos == 64:
            self.mostrar_calculo_tiempo_64()
        else:
            self.lbl_tiempo_real.config(text="")

        return True

    def mostrar_calculo_tiempo_64(self):
        """Calcula el desglose temporal exacto para 64 discos a 1 movimiento por segundo."""
        movimientos = (2 ** 64) - 1
        segundos = movimientos  # Asumiendo 1 movimiento por segundo
        
        minutos = segundos // 60
        horas = minutos // 60
        dias = horas // 24
        anos = dias // 365
        siglos = anos // 100

        texto_tiempo = (
            f"⏳ Para 64 discos se requieren {movimientos:,} movimientos.\n"
            f"A razón de 1 movimiento por segundo, tardaría:\n"
            f"≈ {dias:,} días  |  ≈ {anos:,} años  |  ≈ {siglos:,} siglos ({siglos / 10:.1f} milenios)."
        )
        self.lbl_tiempo_real.config(text=texto_tiempo)

    def dibujar_torres(self):
        self.canvas.delete("all")
        pos_x = {"Origen": 150, "Auxiliar": 350, "Destino": 550}
        
        self.canvas.create_line(50, 250, 650, 250, width=5, fill="#34495e")
        for torre, x in pos_x.items():
            self.canvas.create_line(x, 70, x, 250, width=4, fill="#7f8c8d")
            self.canvas.create_text(x, 270, text=torre, font=("Arial", 11, "bold"), fill="#2c3e50")

        colores = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#1abc9c", "#3498db", "#9b59b6", "#34495e"]
        
        for torre, stack_obj in self.torres.items():
            x_centro = pos_x[torre]
            discos = stack_obj.get_elements()
            altura_disco = max(4, min(20, 200 // max(1, len(discos))))
            
            for i, disco in enumerate(discos):
                ancho = min(120, max(15, disco * (120 / max(1, self.num_discos))))
                y = 240 - (i * altura_disco)
                x1 = x_centro - ancho / 2
                x2 = x_centro + ancho / 2
                y1 = y - (altura_disco - 2)
                y2 = y

                color = colores[(disco - 1) % len(colores)]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=1)
                if altura_disco >= 12:
                    self.canvas.create_text(x_centro, y1 + (altura_disco - 2) / 2, text=str(disco), fill="white", font=("Arial", 8, "bold"))

    def iniciar_animacion(self):
        if self.en_proceso:
            return
        if not self.reiniciar_estructuras():
            return

        if self.num_discos > 25:
            messagebox.showerror("Demasiados discos", "Para más de 25 discos la animación gráfica se congelaría por el límite físico de la pantalla. Usa 'Medir Tiempos' para ver el análisis matemático.")
            return

        self.en_proceso = True
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_rendimiento.config(state=tk.DISABLED)

        self.pasos = []
        self._hanoi_generador(self.num_discos, "Origen", "Destino", "Auxiliar")
        self.ejecutar_siguiente_paso()

    def _hanoi_generador(self, n, origen, destino, auxiliar):
        if n == 1:
            self.pasos.append((origen, destino))
            return
        self._hanoi_generador(n - 1, origen, auxiliar, destino)
        self.pasos.append((origen, destino))
        self._hanoi_generador(n - 1, auxiliar, destino, origen)

    def ejecutar_siguiente_paso(self):
        if self.pasos:
            origen, destino = self.pasos.pop(0)
            
            # Operación de Pila (Stack)
            disco = self.torres[origen].pop()
            self.torres[destino].push(disco)
            self.movimientos_totales += 1
            
            self.dibujar_torres()
            self.lbl_contador.config(text=f"Movimientos: {self.movimientos_totales}")
            
            velocidad = max(5, 300 // max(1, self.num_discos))
            self.root.after(velocidad, self.ejecutar_siguiente_paso)
        else:
            self.en_proceso = False
            self.btn_iniciar.config(state=tk.NORMAL)
            self.btn_rendimiento.config(state=tk.NORMAL)
            messagebox.showinfo("¡Completado!", f"¡Torre de Hanói resuelta en {self.movimientos_totales} movimientos!")

    def medir_tiempos_consola(self):
        discos_prueba = [5, 10, 30, 64]
        print("\n" + "="*60)
        print("ANÁLISIS DE RENDIMIENTO Y TIEMPO - TORRE DE HANÓI (CLASE STACK)")
        print("="*60)

        for d in discos_prueba:
            movimientos = (2 ** d) - 1
            anos = movimientos // (60 * 60 * 24 * 365)
            print(f"Discos: {d:<2} | Movimientos: {movimientos:<22} | Tiempo estimado (1 mov/seg): ~{anos:,} años")

        print("="*60)
        messagebox.showinfo("Medición Completa", "El análisis completo con desglose de días, años y siglos para 64 discos ha sido impreso en la consola.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TorreHanoiPilaApp(root)
    root.mainloop()