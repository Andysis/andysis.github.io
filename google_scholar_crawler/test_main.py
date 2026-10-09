import unittest

from main import parse_profile_html


PROFILE_HTML = """
<html><body>
  <div id="gsc_prf_in">Wang Zhiwei</div>
  <div id="gsc_prf_i"><div class="gsc_prf_il">Huazhong University</div></div>
  <div id="gsc_prf_int"><a>Medical imaging</a></div>
  <table id="gsc_rsb_st"><tbody>
    <tr><td>Citations</td><td class="gsc_rsb_std">1,716</td><td class="gsc_rsb_std">1,100</td></tr>
    <tr><td>h-index</td><td class="gsc_rsb_std">20</td><td class="gsc_rsb_std">16</td></tr>
    <tr><td>i10-index</td><td class="gsc_rsb_std">35</td><td class="gsc_rsb_std">28</td></tr>
  </tbody></table>
  <span class="gsc_g_t">2025</span><span class="gsc_g_al">321</span>
  <table><tbody><tr class="gsc_a_tr">
    <td class="gsc_a_t">
      <a class="gsc_a_at" href="/citations?view_op=view_citation&amp;citation_for_view=LwQcmgYAAAAJ:test">Test Paper</a>
      <div class="gs_gray">A Author, B Author</div>
      <div class="gs_gray">Test Journal, 2025</div>
    </td>
    <td class="gsc_a_c"><a>42</a></td>
    <td class="gsc_a_y"><span>2025</span></td>
  </tr></tbody></table>
</body></html>
"""


class ProfileParserTest(unittest.TestCase):
    def test_parses_profile_metrics_and_publications(self):
        author = parse_profile_html(PROFILE_HTML)

        self.assertEqual(author["name"], "Wang Zhiwei")
        self.assertEqual(author["citedby"], 1716)
        self.assertEqual(author["hindex5y"], 16)
        self.assertEqual(author["cites_per_year"], {2025: 321})
        self.assertEqual(author["publications"][0]["bib"]["title"], "Test Paper")
        self.assertEqual(author["publications"][0]["num_citations"], 42)
        self.assertEqual(
            author["publications"][0]["author_pub_id"], "LwQcmgYAAAAJ:test"
        )

    def test_rejects_block_page(self):
        with self.assertRaisesRegex(RuntimeError, "block/consent"):
            parse_profile_html("<html><body>not a profile</body></html>")


if __name__ == "__main__":
    unittest.main()
