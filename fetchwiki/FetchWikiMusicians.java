import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.htmlparser.Node;
import org.htmlparser.Parser;
import org.htmlparser.Tag;
import org.htmlparser.filters.TagNameFilter;
import org.htmlparser.nodes.TextNode;
import org.htmlparser.tags.Div;
import org.htmlparser.tags.LinkTag;
import org.htmlparser.tags.ParagraphTag;
import org.htmlparser.util.ParserException;
import org.htmlparser.util.SimpleNodeIterator;

public class FetchWikiMusicians implements Runnable {
	Pattern birthpt = Pattern.compile("([0-9]+)年([0-9]+)月([0-9]+)日－"),
			gonept = Pattern.compile("－([0-9]+)年([0-9]+)月([0-9]+)日");
	String baseurl;

	public FetchWikiMusicians(String str) {
		baseurl = str;
	}

	public static void main(String[] args) {
		FetchWikiMusicians tc = new FetchWikiMusicians(
				"http://zh.wikipedia.org/wiki/%E5%8F%A4%E5%85%B8%E9%9F%B3%E6%A8%82%E4%BD%9C%E6%9B%B2%E5%AE%B6%E5%88%97%E8%A1%A8_%28%E6%8C%89%E5%AD%97%E6%AF%8D%E6%8E%92%E5%BA%8F%29");
		new Thread(tc).start();
	}

	@Override
	public void run() {
		try {
			System.out.println("# Fetching " + baseurl);
			int count = 0;
			SimpleNodeIterator sni = new Parser(baseurl)
					.extractAllNodesThatMatch(new TagNameFilter("li"))
					.elements();
			while (sni.hasMoreNodes()) {
				Tag li = (Tag) sni.nextNode();
				Node[] nodes = li.getChildren().toNodeArray();
				LinkTag link = null;
				TextNode txt = null;
				for (Node nd : nodes) {
					if (nd.getClass().getName().endsWith(".LinkTag")) {
						link = (LinkTag) nd;
					} else {
						txt = (TextNode) nd;
					}
				}
				// System.out.println(link.getLink() + "\t" + link.getLinkText()
				// + "\t" + txt.getText());

				SimpleNodeIterator sni1 = new Parser(link.getLink())
						.extractAllNodesThatMatch(new TagNameFilter("div"))
						.elements();
				boolean flag = false;
				String bio = "";
				while (sni1.hasMoreNodes() && !flag) {
					Div div = (Div) sni1.nextNode();
					String clas = div.getAttribute("class");
					if (clas != null && clas.equals("mw-content-ltr")) {
						SimpleNodeIterator sni2 = div.children();
						boolean afterinfo = false;
						while (sni2.hasMoreNodes()) {
							Node nd = sni2.nextNode();
							String ndclassname = nd.getClass().getName();
							if (ndclassname.endsWith("TableTag")) {
								afterinfo = true;
							}
							if (ndclassname.endsWith("ParagraphTag")
									&& afterinfo) {
								ParagraphTag pt = (ParagraphTag) nd;
								// System.out.println(pt.toPlainTextString());
								bio += pt.toPlainTextString() + "\n";
							}
							if (ndclassname.endsWith("HeadingTag") && afterinfo) {
								break;
							}
						}
						if (!afterinfo) {
							System.out.println("Not found: " + link);
						}
						flag = true;
					}
				}
				if (!flag) {
					System.out.println("Not found: " + link);
				}

				String birth = "0000/00/00", gone = "9999/99/99";
				Matcher mat = birthpt.matcher(bio);
				if (mat.find()) {
					birth = mat.group(1) + "/" + mat.group(2) + "/"
							+ mat.group(3);
				}
				mat = gonept.matcher(bio);
				if (mat.find()) {
					gone = mat.group(1) + "/" + mat.group(2) + "/"
							+ mat.group(3);
				}

				BufferedWriter bw = new BufferedWriter(new FileWriter(
						"musicians.txt", true));
				bw.write(birth + "\t" + gone + "\t" + link.getLinkText() + "\t"
						+ txt.getText() + "\t" + link.getLink() + "\t"
						+ bio.replaceAll("\n", "\\\\n"));
				bw.newLine();
				bw.close();

				count++;
				if (count % 50 == 0)
					System.out.println(count);
				Thread.sleep(100);
			}
			System.out.println("Total: " + count);
		} catch (ParserException pe) {
			pe.printStackTrace();
		} catch (InterruptedException ie) {
			ie.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
