import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QCheckBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtGui import QAction
import xml.etree.ElementTree as ET
import json

class MainWindow(QMainWindow):
    json_data = None
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MuSXIIDropGen")

        # Configurar el menú
        self.create_menu()

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout de las 3 columnas superiores
        top_layout = QHBoxLayout()

        # Primera columna (Lista seleccionable 1)
        self.list1 = QListWidget()
        #self.list1.addItems(["Item 1", "Item 2", "Item 3"])
        self.list1.itemSelectionChanged.connect(self.update_second_list)  # Conectar al evento
        top_layout.addWidget(self.list1)

        # Segunda columna (Lista seleccionable 2)
        self.list2 = QListWidget()
        top_layout.addWidget(self.list2)

        # Llenar la segunda lista inicialmente
        self.update_second_list()

        # Tercera columna (CheckBoxes)
        self.check1 = QCheckBox("Exelent")
        self.check2 = QCheckBox("Option")
        self.check3 = QCheckBox("Check 3")
        self.check4 = QCheckBox("Check 4")
        self.check5 = QCheckBox("Check 5")
        self.check6 = QCheckBox("Check 6")
        checkbox_layout = QVBoxLayout()
        checkbox_layout.addWidget(self.check1)
        checkbox_layout.addWidget(self.check2)
        checkbox_layout.addWidget(self.check3)
        checkbox_layout.addWidget(self.check4)
        checkbox_layout.addWidget(self.check5)
        checkbox_layout.addWidget(self.check6)
        top_layout.addLayout(checkbox_layout)

        main_layout.addLayout(top_layout)

        # Botones para agregar y eliminar
        button_layout = QHBoxLayout()
        add_button = QPushButton("➕")  # Botón de agregar
        delete_button = QPushButton("➖")  # Botón de eliminar
        add_button.clicked.connect(self.add_record)
        delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)
        main_layout.addLayout(button_layout)

        # Tabla de registros
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Type", "Item", "Options"])
        main_layout.addWidget(self.table)

        # Botón en la parte inferior derecha
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        finish_button = QPushButton("Generar drop XML")
        bottom_layout.addWidget(finish_button)
        main_layout.addLayout(bottom_layout)

        # Widget principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def update_second_list(self):
        """Actualizar las opciones de la segunda lista según la selección en la primera, utilizando un JSON."""
        # Obtener la selección actual de la primera lista
        selected_items = self.list1.selectedItems()
        if selected_items:
            selection = selected_items[0].text()
            
            # Buscar en el JSON el elemento correspondiente al nombre seleccionado
            matching_item = next((item for item in jsonData if item["Name"] == selection), None)
            
            # Si se encuentra un elemento coincidente, actualizar la segunda lista
            if matching_item:
                subitems = [subitem["Name"] for subitem in matching_item.get("Items", [])]
                self.list2.clear()
                self.list2.addItems(subitems)

    def add_record(self):
        # Obtener datos de las columnas superiores
        col1 = self.list1.currentItem().text() if self.list1.currentItem() else ""
        col2 = self.list2.currentItem().text() if self.list2.currentItem() else ""
        checks = ", ".join([check.text() for check in [self.check1, self.check2, self.check3] if check.isChecked()])

        # Agregar nueva fila a la tabla
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(col1))
        self.table.setItem(row_position, 1, QTableWidgetItem(col2))
        self.table.setItem(row_position, 2, QTableWidgetItem(checks))

    def delete_record(self):
        # Eliminar la fila seleccionada
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)

    def create_menu(self):
        # Crear el menú principal
        menu_bar = self.menuBar()

        # Menú "Archivo"
        file_menu = menu_bar.addMenu("Archivo")

        # Acción "Abrir"
        open_action = QAction("Abrir", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # Acción "Guardar"
        save_action = QAction("Guardar", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Separador
        file_menu.addSeparator()

        # Acción "Salir"
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close_application)
        file_menu.addAction(exit_action)

        # Menú "Ayuda"
        help_menu = menu_bar.addMenu("Ayuda")

        # Acción "Acerca de"
        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_file(self):
        # Acción de abrir archivo (aquí podrías implementar lógica para abrir un archivo)
        QMessageBox.information(self, "Abrir", "Abrir archivo seleccionado.")
        tree = ET.parse("ItemList.xml")
        root = tree.getroot()
        global json_data
        result = []
        for section in root.findall("Section"):
            section_index = section.attrib.get("Index")
            section_name = section.attrib.get("Name")
            items = []

            for item in section.findall("Item"):
                item_index = item.attrib.get("Index")
                item_name = item.attrib.get("Name")
                items.append({"Index": item_index, "Name": item_name})

            result.append({"Index": section_index, "Name": section_name, "Items": items})
        
       
        jsonobj = json.dumps(result)
        json_data = json.loads(jsonobj)
        new_dict = dict()
        for objeto in json_data:
            new_dict[objeto["Index"]] = objeto["Name"]
        
        print(new_dict)
        self.list1.addItems(new_dict.values())

    def save_file(self):
        # Acción de guardar archivo (aquí podrías implementar lógica para guardar un archivo)
        QMessageBox.information(self, "Generar", "Guardar archivo realizado.")

    def close_application(self):
        # Confirmar salida
        respuesta = QMessageBox.question(self, "Salir", "¿Estás seguro de que deseas salir?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if respuesta == QMessageBox.StandardButton.Yes:
            QApplication.quit()

    def show_about(self):
        # Mostrar cuadro de diálogo "Acerca de"
        QMessageBox.information(self, "Acerca de", "Aplicación PyQt6 con menús.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
