from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QPlainTextEdit,
    QTableWidget,
    QLabel,
    QLineEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QTabWidget,
    QSplitter,
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    # Главное окно SQL Editor
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SQL Editor")
        self.resize(1200, 700)
        self._setup_ui()

    def _setup_ui(self) -> None:
        # Основа окна
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Левая панель
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(8)

        db_title = QLabel("Базы данных")
        db_title.setObjectName("dbTitle")

        self.db_tree = QTreeWidget()
        self.db_tree.setHeaderHidden(True)

        # Пример дерева макетов (заглушка)
        db1 = QTreeWidgetItem(["Database"])
        db1_table = QTreeWidgetItem(["table"])
        db1_table1 = QTreeWidgetItem(["table1"])
        db1.addChildren([db1_table, db1_table1])

        db2 = QTreeWidgetItem(["Database1"])
        db2_table = QTreeWidgetItem(["table"])
        db2_table1 = QTreeWidgetItem(["table1"])
        db2.addChildren([db2_table, db2_table1])

        self.db_tree.addTopLevelItems([db1, db2])
        self.db_tree.expandAll()

        left_layout.addWidget(db_title)
        left_layout.addWidget(self.db_tree)

        splitter.addWidget(left_panel)
        splitter.setStretchFactor(0, 1)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(12)

        # Поле для ввода запроса
        sql_title = QLabel("SQL")
        sql_title.setObjectName("sqlTitle")

        self.query_edit = QPlainTextEdit()
        self.query_edit.setPlaceholderText("SELECT * FROM table;")
        self.query_edit.setObjectName("sqlEditor")

        # Кнопка для запуска запроса
        run_row = QHBoxLayout()
        self.btn_run = QPushButton("Run")
        self.btn_run.setObjectName("runButton")
        run_row.addWidget(self.btn_run)
        run_row.addStretch()

        # Строка с выбором: Данные | Структура | История
        tabs = QTabWidget()
        tabs.setObjectName("dataTabs")

        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(0, 0, 0, 0)
        data_layout.setSpacing(8)

        # Строка поиск по результатам запроса
        search_row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("поиск")
        search_row.addWidget(self.search_edit)
        search_row.addStretch()

        # Поле с превью таблицы
        self.result_table = QTableWidget()
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)

        data_layout.addLayout(search_row)
        data_layout.addWidget(self.result_table)

        structure_tab = QWidget()
        structure_layout = QVBoxLayout(structure_tab)
        structure_layout.addWidget(QLabel("Структура таблицы (заглушка)"))

        history_tab = QWidget()
        history_layout = QVBoxLayout(history_tab)
        history_layout.addWidget(QLabel("История запросов (заглушка)"))

        tabs.addTab(data_tab, "Данные")
        tabs.addTab(structure_tab, "Структура")
        tabs.addTab(history_tab, "История")

        self.status_label = QLabel("БД не подключена")
        self.status_label.setObjectName("statusLabel")

        right_layout.addWidget(sql_title)
        right_layout.addWidget(self.query_edit, stretch=2)
        right_layout.addLayout(run_row)
        right_layout.addWidget(tabs, stretch=3)
        right_layout.addWidget(self.status_label)

        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 3)

        root_layout.addWidget(splitter)
        self.setCentralWidget(root)

        self._apply_styles()

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #0F1115;
                color: #FFFFFF;
            }

            QWidget {
                background-color: #0F1115;
                color: #FFFFFF;
                font-family: "JetBrains Mono", monospace;
                font-size: 14px;
            }

            #dbTitle, #sqlTitle {
                font-size: 18px;
            }

            QTreeWidget {
                background-color: #151821;
                border-radius: 6px;
            }

            QPlainTextEdit#sqlEditor {
                background-color: #151821;
                border-radius: 12px;
                padding: 8px;
            }

            QLineEdit {
                background-color: #151821;
                border-radius: 6px;
                padding: 4px 8px;
            }

            QTableWidget {
                background-color: #151821;
                border-radius: 6px;
                gridline-color: #222633;
            }

            QHeaderView::section {
                background-color: #151821;
            }

            QPushButton#runButton {
                background-color: #059669;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 6px 16px;
            }

            QPushButton#runButton:hover {
                background-color: #06b981;
            }

            QTabWidget::pane {
                border: none;
            }

            QTabBar::tab {
                background: #151821;
                padding: 6px 12px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                background: #22D3EE;
                color: #000000;
            }

            QLabel#statusLabel {
                color: #A0A0A0;
                padding-top: 4px;
            }
            """
        )
