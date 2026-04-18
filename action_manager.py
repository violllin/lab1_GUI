import os
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from translations import STRINGS

class ActionManager:
    def __init__(self, window, controller):

        style = window.style()
        self.win = window
        self.ctrl = controller
        base_path = os.path.dirname(__file__)
        cut_icon_path = os.path.join(base_path, "images", "scissors.png")

        self.antlr_run_act = QAction(style.standardIcon(style.StandardPixmap.SP_DesktopIcon), "Run ANTLR", window)

        self.menu_antlr_run = QAction("Запустить ANTLR", window)

        self.new_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileIcon), "", window)
        self.open_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogOpenButton), "", window)
        self.save_act = QAction(style.standardIcon(style.StandardPixmap.SP_DialogSaveButton), "", window)
        self.undo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowBack), "", window)
        self.redo_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowForward), "", window)
        self.copy_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileLinkIcon), "", window)
        self.cut_act = QAction(QIcon(cut_icon_path), "", window)
        self.paste_act = QAction(style.standardIcon(style.StandardPixmap.SP_FileDialogStart), "", window)
        self.run_act = QAction(style.standardIcon(style.StandardPixmap.SP_MediaPlay), "", window)
        self.help_act = QAction(style.standardIcon(style.StandardPixmap.SP_TitleBarContextHelpButton), "", window)
        self.about_act = QAction(style.standardIcon(style.StandardPixmap.SP_MessageBoxInformation), "", window)
        self.zoom_in_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowUp), "", window)
        self.zoom_out_act = QAction(style.standardIcon(style.StandardPixmap.SP_ArrowDown), "", window)

        self.menu_new = QAction("", window)
        self.menu_new.setShortcut(QKeySequence.StandardKey.New)
        self.menu_open = QAction("", window)
        self.menu_open.setShortcut(QKeySequence.StandardKey.Open)
        self.menu_save = QAction("", window)
        self.menu_save.setShortcut(QKeySequence.StandardKey.Save)
        self.menu_save_as = QAction("", window)
        self.menu_save_as.setShortcut("Ctrl+Shift+S")
        self.menu_exit = QAction("", window)
        self.menu_exit.setShortcut("Alt+F4")
        self.menu_run_act = QAction("", window)

        self.menu_undo = QAction("", window)
        self.menu_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self.menu_redo = QAction("", window)
        self.menu_redo.setShortcut(QKeySequence.StandardKey.Redo)
        self.menu_cut = QAction("", window)
        self.menu_cut.setShortcut(QKeySequence.StandardKey.Cut)
        self.menu_copy = QAction("", window)
        self.menu_copy.setShortcut(QKeySequence.StandardKey.Copy)
        self.menu_paste = QAction("", window)
        self.menu_paste.setShortcut(QKeySequence.StandardKey.Paste)
        self.menu_delete = QAction("", window)
        self.menu_delete.setShortcut(QKeySequence.StandardKey.Delete)
        self.menu_select_all = QAction("", window)
        self.menu_select_all.setShortcut(QKeySequence.StandardKey.SelectAll)

        self.menu_help = QAction("", window)
        self.menu_help.setShortcut('F1')
        self.menu_about = QAction("", window)

        self.doc_actions = {}
        doc_keys = ["task", "grammar", "classification", "method",
                    "neutralization", "test_case", "references", "source_code"]
        for key in doc_keys:
            action = QAction("", window)
            action.triggered.connect(lambda checked, k=key: self.ctrl.show_document(k))
            self.doc_actions[key] = action
        self.text_actions = []

        self.help_info_act = QAction("Вызов справки", window)
        self.help_info_act.triggered.connect(lambda: self.ctrl.show_document("help"))

        self.retranslate_actions("ru")
        self._connect_signals()

    def retranslate_actions(self, lang):
        s = STRINGS[lang]
        doc_map = {
            "task": "doc_task",
            "grammar": "doc_grammar",
            "classification": "doc_classification",
            "method": "doc_method",
            "neutralization": "doc_neutralization",
            "test_case": "doc_test_case",
            "references": "doc_references",
            "source_code": "doc_source_code"
        }
        for key, lang_key in doc_map.items():
            if key in self.doc_actions:
                self.doc_actions[key].setText(s.get(lang_key, key))

        self.new_act.setText(s["action_new"])
        self.open_act.setText(s["action_open"])
        self.save_act.setText(s["action_save"])
        self.undo_act.setText(s["action_undo"])
        self.redo_act.setText(s["action_redo"])
        self.copy_act.setText(s["action_copy"])
        self.cut_act.setText(s["action_cut"])
        self.paste_act.setText(s["action_paste"])

        self.run_act.setText(s["menu_run_par"])
        self.antlr_run_act.setText(s["menu_antlr_run"])

        self.help_act.setText(s["menu_help"])
        self.zoom_in_act.setText(s["action_zoom_in"])
        self.zoom_out_act.setText(s["action_zoom_out"])
        self.about_act.setText(s["action_about"])
        self.about_act.setStatusTip(s["action_about"])
        self.menu_new.setText(s["action_new"])
        self.menu_open.setText(s["action_open"])
        self.menu_save.setText(s["action_save"])
        self.menu_save_as.setText(s["action_save_as"])
        self.menu_exit.setText(s["action_exit"])
        self.menu_run_act.setText(s["menu_run"])
        self.menu_undo.setText(s["action_undo"])
        self.menu_redo.setText(s["action_redo"])
        self.menu_cut.setText(s["action_cut"])
        self.menu_copy.setText(s["action_copy"])
        self.menu_paste.setText(s["action_paste"])
        self.menu_delete.setText(s["action_delete"])
        self.menu_select_all.setText(s["action_select_all"])
        self.menu_help.setText(s["action_help"])
        self.menu_about.setText(s["action_about"])


    def _connect_signals(self):

        self.antlr_run_act.triggered.connect(self.ctrl.run_antlr_analysis)
        self.menu_antlr_run.triggered.connect(self.ctrl.run_antlr_analysis)

        self.new_act.triggered.connect(self.ctrl.file_new)
        self.menu_new.triggered.connect(self.ctrl.file_new)
        self.open_act.triggered.connect(self.ctrl.file_open)
        self.menu_open.triggered.connect(self.ctrl.file_open)
        self.save_act.triggered.connect(self.ctrl.file_save)
        self.menu_save.triggered.connect(self.ctrl.file_save)
        self.menu_save_as.triggered.connect(self.ctrl.file_save_as)
        self.menu_exit.triggered.connect(self.win.close)
        self.menu_delete.triggered.connect(lambda: self.win.get_current_editor().clear() if self.win.get_current_editor() else None)
        self.undo_act.triggered.connect(lambda: self.win.get_current_editor().undo() if self.win.get_current_editor() else None)
        self.menu_undo.triggered.connect(lambda: self.win.get_current_editor().undo() if self.win.get_current_editor() else None)
        self.redo_act.triggered.connect(lambda: self.win.get_current_editor().redo() if self.win.get_current_editor() else None)
        self.menu_redo.triggered.connect(lambda: self.win.get_current_editor().redo() if self.win.get_current_editor() else None)
        self.copy_act.triggered.connect(lambda: self.win.get_current_editor().copy() if self.win.get_current_editor() else None)
        self.menu_copy.triggered.connect(lambda: self.win.get_current_editor().copy() if self.win.get_current_editor() else None)
        self.cut_act.triggered.connect(lambda: self.win.get_current_editor().cut() if self.win.get_current_editor() else None)
        self.menu_cut.triggered.connect(lambda: self.win.get_current_editor().cut() if self.win.get_current_editor() else None)
        self.paste_act.triggered.connect(lambda: self.win.get_current_editor().paste() if self.win.get_current_editor() else None)
        self.menu_paste.triggered.connect(lambda: self.win.get_current_editor().paste() if self.win.get_current_editor() else None)
        self.menu_select_all.triggered.connect(lambda: self.win.get_current_editor().selectAll() if self.win.get_current_editor() else None)
        self.zoom_in_act.triggered.connect(self.ctrl.zoom_in)
        self.zoom_out_act.triggered.connect(self.ctrl.zoom_out)
        self.help_act.triggered.connect(self.ctrl.show_help)
        self.menu_help.triggered.connect(self.ctrl.show_help)
        self.about_act.triggered.connect(self.ctrl.show_about)
        self.menu_about.triggered.connect(self.ctrl.show_about)
        self.run_act.triggered.connect(self.ctrl.run_lexer)
        self.menu_run_act.triggered.connect(self.ctrl.run_lexer)