from pdf_tools import Page, Rectangle, Line
import typer

def draw_note(page, rect, text, pos=None, vertical_text_align="top"):
    rect = rect.apply_margin(2,2)
    page.draw_rect_humanized(rect, stroke_width=0.8, stroke_color=0.0)
    if "|" in text:
        title, text = text.split("|")
        text = text.lstrip()
        title_rect, rect = rect.top_partition(height=8, gap=2)
        page.draw_text_aligned(title, title_rect, font="SouvenirBold", font_size=12, small_caps=True)
        page.draw_line(Line.from_center_and_width(title_rect.bottom_center(), 20))
        #page.draw_rect_humanized(title_rect, stroke_width=0.8, stroke_color=0.0)
         
    page.layout_text_aligned(text, rect.apply_margin(x=2, bottom=2), font="RobotoSlab", font_size=10, vertical_align=vertical_text_align)


def draw_board(page, title, notes, grid=(3,5), vertical_text_align="top", landscape=True, pagesize=Page.A4):
    page.set_pagesize(pagesize, landscape=landscape)

    header, body = page.page_rect.top_partition(0.1)
    page.draw_text_aligned(title, header, font="SouvenirBold", font_size=24, small_caps=True)
    rects = body.subdivide(*grid)

    counter = 0
    for i, note in enumerate(notes):
        r = rects[i]
        draw_note(page, r, note, vertical_text_align=vertical_text_align)

    page.new_page()


def main():
    page = Page("pdf/board.pdf", pagesize=Page.A4, landscape=True)

    todo = [
        "
        "Design skeleton encounter",
    ]

    draw_board( page, "Todo", todo, grid=(8,2), pagesize=Page.A5, landscape=False, vertical_text_align="center")
    draw_board(
        page,
        "Prologue: The Halls of Diras",
        [
            "Gundren contacts Tombur. Meet me at Halls of Diras",

            "The Halls of Diras are a legendary place for your dwarven folk. Here, the great warrior Diras the Elder was layed to rest among his fellow shield brothers.",

            "Deep in the forest of Eldenmore you meet Gundren at the ancient crossroads beside...",

            "Entrance | Suddenly the forrest clears and you stand before a cliff face. Rough steps have been hewn from the rocks. The face of an old dwarf has been carved into the rock face, its eyes staring at you make you feel uneasy. Inscription: \"Only my brethren free of deceit shall enter.\" \"The others shall perish in tears.\"", 
            "First Room: Entrance Tunnel | Traps against grave robbers. Alternative: Ochre Slimes wait on the ceiling of the corridor for unsuspecting victims.",
            "Second Room: Sarcophagus | Riddle to open secret door:<br/>\"Offer me your life or turn around.\"",
            "Third Room: | Sliding Puzzle, Encounter with Skeletons. <br/> The missing tile fits into the open slot perfectly with a satisfying chink. You wait in anticipation but nothing further happens. Suddenly you hear a scraping noise all around you as the walls begin to move upwards. In horror you realise that it was not some random symbol that you assembled, as the skeletons attack...",
            "Fourth Room | Location of Puzzle Box"
        ]
    )
    draw_board(
        page,
        "Part ii: Phandelver",
        [

            """Letter to Glasstaff| Your intel was correct - the dwarf brought the Lords' Alliance into the fold. Fortunately, the ambush was a success and the goblins captured both the dwarf and the sellsword. They transported the dwarf to their leader and my emissary is en route to Cragmaw Castle now to take care of THAT loose end.<br/> Beware though - my spies in Neverwinter informed me that the dwarf hired a separate group of adventurers to escort his mining supplies to Phandalin. They may begin asking questions once they arrive. Capture them if you can, kill them if you must, but don't allow them to upset our plans.<br/> I'm counting on you, Iarno. Don't disappoint me.""",
        ],
        (2,4)
    )
    draw_board(
        page,
        "Part iii: Into the Spider's Web",
        [
            """Quest: Wyvern Tor | Defeat the orcs""",
        ],
        (2,3)
    )
    page.save()


if __name__ == "__main__":
    typer.run(main)

