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
    QFileDialog,
    QTableWidgetItem,
    QSizePolicy,
    QHeaderView,
)

from PyQt6.QtCore import Qt
from sql_editor.db.connection import Database


class MainWindow(QMainWindow):
    """Главное окно SQL Editor.
    Реализует подключение к SQLite и выполнение SELECT-запросов.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SQL Editor")
        self.resize(1200, 700)

        self._db = Database()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        # Корневой контейнер
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
        self.db_tree.addTopLevelItem(QTreeWidgetItem(["Нет подключений"]))

        left_layout.addWidget(db_title)
        left_layout.addWidget(self.db_tree)
        splitter.addWidget(left_panel)
        splitter.setStretchFactor(0, 1)

        # Правая панель
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(12)

        # Верхняя строка: кнопка подключения
        top_row = QHBoxLayout()
        self.btn_connect = QPushButton("Подключить БД")
        self.btn_connect.setObjectName("connectButton")
        self.status_label = QLabel("БД не подключена")
        self.status_label.setObjectName("statusLabel")

        top_row.addWidget(self.btn_connect)
        top_row.addStretch()
        top_row.addWidget(self.status_label)

        # SQL-запрос
        sql_title = QLabel("SQL")
        sql_title.setObjectName("sqlTitle")

        self.query_edit = QPlainTextEdit()
        self.query_edit.setPlaceholderText("Введите SQL-запрос (например SELECT * FROM table;)")
        self.query_edit.setObjectName("sqlEditor")

        # Кнопка выполнения
        run_row = QHBoxLayout()
        self.btn_run = QPushButton("Run")
        self.btn_run.setObjectName("runButton")
        run_row.addWidget(self.btn_run)
        run_row.addStretch()

        # Табы (Данные | Структура | История)
        tabs = QTabWidget()
        tabs.setObjectName("dataTabs")

        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)
        data_layout.setContentsMargins(0, 0, 0, 0)
        data_layout.setSpacing(8)

        search_row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("поиск")
        search_row.addWidget(self.search_edit)
        search_row.addStretch()

        # Поле с превью таблицы
        self.result_table = QTableWidget()
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)

        # важно: таблица должна растягиваться
        self.result_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

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

        # Компоновка правой панели
        right_layout.addLayout(top_row)
        right_layout.addWidget(sql_title)
        right_layout.addWidget(self.query_edit, stretch=2)
        right_layout.addLayout(run_row)
        right_layout.addWidget(tabs, stretch=3)

        splitter.addWidget(right_panel)
        splitter.setStretchFactor(1, 3)

        root_layout.addWidget(splitter)
        self.setCentralWidget(root)

        self._apply_styles()

    # ------------------ Логика ------------------
    def _connect_signals(self) -> None:
        # noinspection PyUnresolvedReferences
        self.btn_connect.clicked.connect(self._on_connect_db)
        # noinspection PyUnresolvedReferences
        self.btn_run.clicked.connect(self._on_run_query)

    def _on_connect_db(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл базы данных SQLite",
            "",
            "SQLite Database (*.db *.sqlite *.sqlite3);;All Files (*)",
        )
        if not path:
            return

        try:
            self._db.connect(path)
        except Exception as exc:
            self.status_label.setText(f"Ошибка подключения: {exc}")
            return

        # Загружаем список таблиц
        try:
            tables = self._db.get_tables()
        except Exception as exc:
            self.status_label.setText(f"Ошибка чтения таблиц: {exc}")
            return

        # Обновляем дерево
        self.db_tree.clear()
        db_item = QTreeWidgetItem([path.split("/")[-1]])
        for table in tables:
            db_item.addChild(QTreeWidgetItem([table]))
        self.db_tree.addTopLevelItem(db_item)
        self.db_tree.expandAll()

        self.status_label.setText(f"Подключено: {path.split("/")[-1]}")


    def _on_run_query(self) -> None:
        query = self.query_edit.toPlainText().strip()
        if not query:
            self.status_label.setText("Введите SQL-запрос")
            return

        if not self._db.is_connected():
            self.status_label.setText("Сначала подключите базу данных")
            return

        if not query.lower().startswith("select"):
            self.status_label.setText("На этом этапе поддерживаются только SELECT-запросы")
            return

        try:
            col_names, rows = self._db.execute_select(query)
        except Exception as exc:
            self.status_label.setText(f"Ошибка выполнения: {exc}")
            return

        self._fill_table(col_names, rows)
        self.status_label.setText(f"Выведено строк: {len(rows)}")

    def _fill_table(self, col_names, rows) -> None:
        self.result_table.clear()
        self.result_table.setRowCount(len(rows))
        self.result_table.setColumnCount(len(col_names))
        self.result_table.setHorizontalHeaderLabels(col_names)

        for r_idx, row in enumerate(rows):
            for c_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemFlag.ItemIsEditable)

                # если значение числовое — выравниваем вправо
                if isinstance(value, (int, float)):
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                self.result_table.setItem(r_idx, c_idx, item)

    # ------------------ Стили ------------------
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

            QTableCornerButton::section {
                background-color: #151821;
                border: none;
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
