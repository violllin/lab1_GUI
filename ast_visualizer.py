from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QColor, QPen, QBrush, QFont, QPainter
from ast_nodes import LetNode, LambdaNode, ParamNode, BinOpNode, VarNode, LiteralNode


class ASTVisualizer(QDialog):
    def __init__(self, ast_root, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Визуализация AST")
        self.resize(1200, 800)

        self.COLORS = {
            "bg": QColor("#FFFFFF"),
            "border": QColor("#000000"),
            "text": QColor("#000000"),
            "line": QColor("#000000")
        }

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.NODE_WIDTH = 180
        self.NODE_HEIGHT = 70
        self.X_SPACING = 40
        self.Y_SPACING = 120

        tree_data = self.build_detailed_tree(ast_root)
        if tree_data:
            self.compute_layout(tree_data)
            self.assign_coordinates(tree_data, 0, 0)
            self.draw_edges(tree_data)
            self.draw_nodes(tree_data)

    def _create_node(self, label):
        return {
            "label": label,
            "children": []
        }

    def build_detailed_tree(self, node):
        if not node: return None

        if isinstance(node, LetNode):
            root = self._create_node("LET DECLARATION")
            name_val = node.name_tok.lexeme if node.name_tok else "???"
            root["children"].append(self._create_node(f"ID: {name_val}"))
            if node.lambda_node:
                root["children"].append(self.build_detailed_tree(node.lambda_node))
            return root

        elif isinstance(node, LambdaNode):
            root = self._create_node("LAMBDA FUNCTION")
            if node.params:
                params_root = self._create_node(f"PARAMS ({len(node.params)})")
                for p in node.params:
                    params_root["children"].append(self.build_detailed_tree(p))
                root["children"].append(params_root)

            ret_type = node.return_type_tok.lexeme if node.return_type_tok else "infer"
            root["children"].append(self._create_node(f"RETURNS: {ret_type}"))

            if node.body:
                body_root = self._create_node("BODY")
                body_root["children"].append(self.build_detailed_tree(node.body))
                root["children"].append(body_root)
            return root

        elif isinstance(node, ParamNode):
            name = node.name_tok.lexeme if node.name_tok else "?"
            ptype = node.type_tok.lexeme if node.type_tok else "?"
            return self._create_node(f"{name} : {ptype}")

        elif isinstance(node, BinOpNode):
            op_str = node.op_tok.lexeme if node.op_tok else "?"
            root = self._create_node(f"OPERATOR: {op_str}")
            if node.left: root["children"].append(self.build_detailed_tree(node.left))
            if node.right: root["children"].append(self.build_detailed_tree(node.right))
            return root

        elif isinstance(node, VarNode):
            return self._create_node(node.token.lexeme)

        elif isinstance(node, LiteralNode):
            return self._create_node(f"VALUE: {node.token.lexeme}")

        return None

    def compute_layout(self, node):
        if not node["children"]:
            node["width"] = self.NODE_WIDTH
            return self.NODE_WIDTH
        children_width = sum(self.compute_layout(c) for c in node["children"])
        children_width += self.X_SPACING * (len(node["children"]) - 1)
        node["width"] = max(self.NODE_WIDTH, children_width)
        return node["width"]

    def assign_coordinates(self, node, x, y):
        node["x"], node["y"] = x, y
        if not node["children"]: return
        total_width = sum(c["width"] for c in node["children"]) + self.X_SPACING * (len(node["children"]) - 1)
        current_x = x - total_width / 2
        for child in node["children"]:
            child_width = child["width"]
            self.assign_coordinates(child, current_x + child_width / 2, y + self.Y_SPACING)
            current_x += child_width + self.X_SPACING

    def draw_edges(self, node):
        pen = QPen(self.COLORS["line"], 2)
        for child in node["children"]:
            self.scene.addLine(
                node["x"], node["y"] + self.NODE_HEIGHT / 2,
                child["x"], child["y"] - self.NODE_HEIGHT / 2,
                pen
            )
            self.draw_edges(child)

    def draw_nodes(self, node):
        rect_x = node["x"] - self.NODE_WIDTH / 2
        rect_y = node["y"] - self.NODE_HEIGHT / 2

        self.scene.addRect(rect_x, rect_y, self.NODE_WIDTH, self.NODE_HEIGHT,
                           QPen(self.COLORS["border"], 2), QBrush(self.COLORS["bg"]))

        label_item = QGraphicsTextItem(node["label"])
        label_item.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        label_item.setDefaultTextColor(self.COLORS["text"])
        label_item.setTextWidth(self.NODE_WIDTH - 10)

        option = label_item.document().defaultTextOption()
        option.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_item.document().setDefaultTextOption(option)

        br = label_item.boundingRect()
        label_item.setPos(node["x"] - br.width() / 2, node["y"] - br.height() / 2)
        self.scene.addItem(label_item)

        for child in node["children"]:
            self.draw_nodes(child)

    def wheelEvent(self, event):
        factor = 1.2 if event.angleDelta().y() > 0 else 0.8
        self.view.scale(factor, factor)