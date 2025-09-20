from PySide6.QtCore import Qt, QPoint, QRect, QObject
from PySide6.QtWidgets import QWidget

class FramelessHelper(QObject):
    """Attach to any QWidget to give it native-like resize & move."""
    def __init__(self, target: QWidget, /, border=6):
        super().__init__()
        self._tgt = target
        self._bd = border
        self._region = None
        self._click_pos = None
        self._start_geo = None
        target.setMouseTracking(True)
        target.installEventFilter(self)

    def eventFilter(self, obj, ev):
        if obj is not self._tgt:
            return False
        if ev.type() == ev.Type.MouseButtonPress and ev.button() == Qt.LeftButton:
            self._click_pos = ev.globalPosition().toPoint()
            self._start_geo = self._tgt.geometry()
            self._region = self._calc_region(ev.position().toPoint())
            return False

        if ev.type() == ev.Type.MouseButtonRelease:
            self._click_pos = self._start_geo = self._region = None
            return False

        if ev.type() == ev.Type.MouseMove:
            pos = ev.position().toPoint()
            # no button -> only update cursor
            if self._click_pos is None:
                self._tgt.setCursor(self._cursor_shape(self._calc_region(pos)))
                return False
            # with button -> resize or move
            delta = ev.globalPosition().toPoint() - self._click_pos
            g = QRect(self._start_geo)
            r = self._region
            if r == Qt.LeftEdge:
                g.setLeft(g.left() + delta.x())
            elif r == Qt.RightEdge:
                g.setRight(g.right() + delta.x())
            elif r == Qt.TopEdge:
                g.setTop(g.top() + delta.y())
            elif r == Qt.BottomEdge:
                g.setBottom(g.bottom() + delta.y())
            elif r == Qt.TopLeftCorner:
                g.setTopLeft(g.topLeft() + delta)
            elif r == Qt.TopRightCorner:
                g.setTopRight(g.topRight() + delta)
            elif r == Qt.BottomLeftCorner:
                g.setBottomLeft(g.bottomLeft() + delta)
            elif r == Qt.BottomRightCorner:
                g.setBottomRight(g.bottomRight() + delta)
            else:  # move
                g.moveTopLeft(g.topLeft() + delta)
            if g.width() >= self._tgt.minimumWidth() and g.height() >= self._tgt.minimumHeight():
                self._tgt.setGeometry(g)
            return True
        return False

    def _calc_region(self, pos: QPoint):
        r = self._tgt.rect()
        m = self._bd
        x, y = pos.x(), pos.y()
        if x < m and y < m:
            return Qt.TopLeftCorner
        if x >= r.right() - m and y < m:
            return Qt.TopRightCorner
        if x < m and y >= r.bottom() - m:
            return Qt.BottomLeftCorner
        if x >= r.right() - m and y >= r.bottom() - m:
            return Qt.BottomRightCorner
        if x < m:
            return Qt.LeftEdge
        if x >= r.right() - m:
            return Qt.RightEdge
        if y < m:
            return Qt.TopEdge
        if y >= r.bottom() - m:
            return Qt.BottomEdge
        return 0  # inside

    def _cursor_shape(self, region):
        return {
            Qt.LeftEdge: Qt.SizeHorCursor,
            Qt.RightEdge: Qt.SizeHorCursor,
            Qt.TopEdge: Qt.SizeVerCursor,
            Qt.BottomEdge: Qt.SizeVerCursor,
            Qt.TopLeftCorner: Qt.SizeFDiagCursor,
            Qt.TopRightCorner: Qt.SizeBDiagCursor,
            Qt.BottomLeftCorner: Qt.SizeBDiagCursor,
            Qt.BottomRightCorner: Qt.SizeFDiagCursor,
        }.get(region, Qt.ArrowCursor)