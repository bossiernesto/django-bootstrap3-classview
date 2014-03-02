"""
.. module:: css to less converter
   :platform: independent
   :synopsis: a small script for converting css files to less one.
   :copyright: (c) 2014 by Ernesto Bossi.
   :license: BSD-3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>

.. note :: special thanks to Thomas Pierson <contact@thomaspierson.fr> , Marcin Kulik <m@ku1ik.com> for this great idea.
"""

#CSS Official colors
CSS_COLORS = ['aliceblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black','blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod','darkgray','darkgrey','darkgreen','darkkhaki','darkmagenta','darkolivegreen','darkorange','darkorchid','darkred','darksalmon','darkseagreen','darkslateblue','darkslategray','darkslategrey','darkturquoise','darkviolet','deeppink','deepskyblue','dimgray','dimgrey','dodgerblue','firebrick','floralwhite','forestgreen','fuchsia','gainsboro','ghostwhite','gold','goldenrod','gray','grey','green','greenyellow','honeydew','hotpink','indianred','indigo','ivory','khaki','lavender','lavenderblush','lawngreen','lemonchiffon','lightblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgray','lightgrey','lightgreen','lightpink','lightsalmon','lightseagreen','lightskyblue','lightslategray','lightslategrey','lightsteelblue','lightyellow','lime','limegreen','linen','magenta','maroon','mediumaquamarine','mediumblue','mediumorchid','mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise','mediumvioletred','midnightblue','mintcream','mistyrose','moccasin','navajowhite','navy','oldlace','olive','olivedrab','orange','orangered','orchid','palegoldenrod','palegreen','paleturquoise','palevioletred','papayawhip','peachpuff','peru','pink','plum','powderblue','purple','red','rosybrown','royalblue','saddlebrown','salmon','sandybrown','seagreen','seashell','sienna','silver','skyblue','slateblue','slategray','slategrey','snow','springgreen','steelblue','tan','teal','thistle','tomato','turquoise','violet','wheat','white','whitesmoke','yellow','yellowgreen']

VENDOR_PREFIXES_LIST = ['-moz','-o','-ms','-webkit']
VENDOR_PREFIXES = "^(-moz|-o|-ms|-webkit)-"

class CSSConverter(object):

    def __init__(self, css=None, options={}):
        self.css = css
        self.tree = {}
        self.less = None
        self.colors = {}
        self.vendor_mixins = {}
        self.options = {}
        self.options.update({"update_colors": False, "vendor_mixins": False})
        self.options.update(options)

    def cleanup(self):
        self.tree = {}
        self.less = ''

    def process_less(self):
        self.cleanup()
        if not self.css:
            return False
        self.generate_tree()
        self.render_less()
        return True

    def get_less(self):
        return self.less

    def set_css(self, css):
        self.css = css




    # Split set of rules into single item
    def convert_rules(data)
      data.split(';').map { |s| s.strip }.reject { |s| s.empty? }
    end

    def color?(value)
      if CSS_COLORS.include?(value.strip) || /^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$/.match(value.strip) != nil ||
        /(rgba?)\(.*\)/.match(value)
        true
      else
        false
      end
    end

    # Check if the global index contains the color and replace the value
    # accordingly
    def convert_if_color(color)
      if color?(color)
        unless @colors.key?(color.strip)
          @colors[color.strip] = "@color#{@colors.size}"
        end
        @colors[color.strip]
      else
        color
      end
    end

    # Try to match a color of a set of rules
    def match_color(style)
      convert_rules(style).map { |r|
        (key, value) = r.split(":").map { |e| e.strip }
        if value.nil?
          "#{key}"
        else
          "#{key}: #{value.split(/\s+/).map { |e| convert_if_color(e) }.join(" ")}"
        end
      }.join(";\n") << ";\n"
    end

    def match_vendor_prefix_mixin(style)
      normal_rules = {}
      prefixed_rules = {}

      # First identify all those vendor prefixed rules that are similar
      convert_rules(style).each { |e|
        (key, value) = e.split(":").map { |e| e.strip }
        if value.nil?
          normal_rules[key] = nil
        else
          # If this is a vendor prefixed rule, collect all similar ones in a
          # single entry
          if key.match(VENDOR_PREFIXES)
            rule_key = key.gsub(VENDOR_PREFIXES, "")
            val = value.split(/\s+/).map { |e| e.strip }

            if prefixed_rules.key?(rule_key) && prefixed_rules[rule_key] != val
              # Abort, because we have different values for different vendor
              # prefixed values, this can only mean intended different behavior
              # for different browsers
              return style
            end

            prefixed_rules[rule_key] = val
          else
            normal_rules[key] = value
          end
        end
      }

      # Now we have all information to proceed. First, we check if the mixin is
      # already available globally. If not we announce it
      prefixed_rules.each { |k,v|
        unless @vendor_mixins.key?(k)
          @vendor_mixins[k] = v.size
        end

        if normal_rules.key?(k)
          normal_rules.delete(k)
          normal_rules[".vp-#{k}(#{v.join("; ")})"] = nil
        end
      }

      result = normal_rules.to_a.map { |e|
        val = "#{e[0]}"
        val << ": #{e[1]}" unless e[1].nil?
        val}.join(";\n") << ";\n"
    end

    # This method is called for each selector that we want to add as a rule.
    # Since we have plain CSS rules here, we should try to bring some order into
    # the chaos.
    def add_rule(tree, selectors, style)
      return if style.nil? || style.empty?

      # Stop recursion and add styles
      if selectors.empty?

        # Match and replace global colors
        style = match_color(style) if @options[:update_colors]

        # Match and replace global mixins for vendor specific behavior
        style = match_vendor_prefix_mixin(style) if @options[:vendor_mixins]

        (tree[:style] ||= ';') << style
      else
        first, rest = selectors.first, selectors[1..-1]
        node = (tree[first] ||= {})
        add_rule(node, rest, style)
      end
    end

    def generate_tree
      @css.split("\n").map { |l| l.strip }.join.gsub(/\/\*+[^\*]*\*+\//, '').split(/[\{\}]/).each_slice(2) do |style|
        rules = style[0].strip
        # handle child selector case - step1
        if rules.include?('>')
          rules = rules.gsub(/\s*>\s*/, ' &>')
        end
        if rules.include?("@import")
          import_rule = rules.match(/@import.*;/)[0]
          rules = rules.gsub(/@import.*;/, '')
          add_rule(@tree, [], import_rule)
        end
        # leave multiple rules alone
        if rules.include?(',')
          add_rule(@tree, [rules], style[1])
        else
          rules_split = rules.split(/\s+/)
          # handle child selector case - step2
          rules_split.map! {|rule| rule.gsub('&>', '& > ')}
          add_rule(@tree, rules_split, style[1])
        end
      end
    end


    def build_mixin_list(indent)
      less = ""
      @vendor_mixins.each { |k,v|
          args = Array(0..v-1).map { |e| "@p#{e}" }
          less << ".vp-#{k}(#{args.join("; ")}) {\n"
          VENDOR_PREFIXES_LIST.each { |vp|
            less << " " * (indent+4) << "#{vp}-#{k}: #{args.join(" ")};\n"
          }
          less << " " * (indent+4) << "#{k}: #{args.join(" ")};\n"
          less << "}\n"
        }
      less << "\n"
    end

    def render_less(tree=nil, indent=0)
      if tree.nil?
        # This is the initial node, add all global vars / mixins here
        @colors.each { |k,v|
          @less << "#{v}: #{k};\n"
        }
        @less << "\n" if @colors.size > 0

        @less << build_mixin_list(indent) if @options[:vendor_mixins]

        tree = @tree
      end
      tree.each do |element, children|
        if element == :style
          @less = @less + convert_rules(children).map { |s| s + ";" }.join("\n") + "\n"
        else
          @less = @less + ' ' * indent + element + " {\n"
          style = children.delete(:style)
          if style
            @less = @less + convert_rules(style).map { |s| ' ' * (indent+4) + s + ";" }.join("\n") + "\n"
          end
          render_less(children, indent + 4)
          @less = @less + ' ' * indent + "}\n"
        end
      end
    end

  end

end