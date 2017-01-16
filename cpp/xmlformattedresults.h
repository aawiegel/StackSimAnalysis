#ifndef XMLFORMATTEDRESULTS_H
#define XMLFORMATTEDRESULTS_H

#include <QXmlStreamWriter>
#include <QFile>

#include "textformattedresults.h"
#include "simulationresults.h"
#include "reactionschemediagram.h"
#include "fixedreactionschemediagram.h"


class XMLFormattedResults
{
public:
    XMLFormattedResults( ReactionSchemeDiagram* pSchemeDiagram );
    XMLFormattedResults( FixedReactionSchemeDiagram* pSchemeDiagram );

    void writeResults();

    void setDelimiter( enum TEXT_FORMAT_STYLE d );

    bool isScheme3D() { return scheme3D; }

    void openFileDialog();

protected:

    ReactionSchemeDiagram* scheme_diagram;
    FixedReactionSchemeDiagram* fixed_scheme_diagram;
    ReactionScheme* scheme;

    bool scheme3D;

    enum TEXT_FORMAT_STYLE format_style;
    QChar separator;

    virtual void writeHeader();
    virtual void writeSchemeData();
    virtual void writeData();
    void setOutputFile(QFile &file );
    virtual void formatRawData(QTextStream& data_in, FloatArray& data_array );

    //virtual void writeFooter();

    int num_compartments;
    int num_columns;
    int num_layers;
    int num_rows;
    unsigned int num_species;
    unsigned int num_points;

    SimulationResult* results;
    QXmlStreamWriter xmlWriter;


};



#endif // XMLFORMATTEDRESULTS_H
